import asyncio
from typing import List, Dict, Any

from database.service.character_service import get_all_characters
from database.service.character_server_service import get_sorted_characters_by_server
from database.service.dungeon_service import get_all_current_season_dungeons
from database.service.dungeon_run_service import get_all_dungeon_runs_for_character
from database.models.dungeon_run import DungeonRun
from database.models.character import Character
from utils.api.request_character_information import get_multiple_wow_characters
from utils.get_nested_dict_or_return_empty import get_nested_dict_or_return_empty
from settings import CURRENT_SEASON_SCORE

try:
    # Tortoise ORM transaction utils
    from tortoise.transactions import in_transaction
except ImportError:  # Fallback if transaction manager is not available
    in_transaction = None  # type: ignore


# Keep this a constant 64-bit integer; must be consistent across instances
ADVISORY_LOCK_KEY = 812345678901


async def get_current_season_dungeons() -> Dict[str, int]:
    return {d.short_name.lower(): d.id for d in await get_all_current_season_dungeons()}


def _add_dungeon_details(new_score: int, new_run: dict, updated_runs: List[dict]) -> None:
    updated_runs.append(
        {
            "name": new_run.get("dungeon"),
            "mythic_level": new_run.get("mythic_level"),
            "num_keystone_upgrades": new_run.get("num_keystone_upgrades"),
            "clear_time_ms": new_run.get("clear_time_ms"),
            "par_time_ms": new_run.get("par_time_ms"),
            "score": new_score,
        }
    )


async def get_character_updated_dungeon_runs(
    character_id: int, updated_dungeon_runs: List[dict], current_season_dungeons: Dict[str, int]
) -> List[dict]:
    updated_runs: List[dict] = []
    db_runs = await get_all_dungeon_runs_for_character(character_id)

    if not db_runs:
        for run in updated_dungeon_runs:
            score = run.get("score", 0)
            if score > 0:
                _add_dungeon_details(score, run, updated_runs)
        return updated_runs

    # Compare by dungeon id
    remaining = list(updated_dungeon_runs)
    for db_run in db_runs:
        next_remaining = []
        for new_run in remaining:
            score = new_run.get("score", 0)
            if score == 0:
                continue
            dungeon_id = current_season_dungeons.get(new_run.get("short_name", "").lower())
            if dungeon_id == db_run.dungeon_id:
                if score > db_run.score:
                    _add_dungeon_details(score, new_run, updated_runs)
            else:
                next_remaining.append(new_run)
        remaining = next_remaining

    for run in remaining:
        score = run.get("score", 0)
        if score > 0:
            _add_dungeon_details(score, run, updated_runs)

    return updated_runs


async def add_score_differs_to_characters(
    fetched: List[dict], db_characters: List[dict], current_season_dungeons: Dict[str, int]
) -> List[dict]:
    output: List[dict] = []

    # Index DB characters for O(1) lookup by (region, realm, name)
    idx: Dict[tuple, dict] = {}
    for c in db_characters:
        key = (c.get("region", "").lower(), c.get("realm", "").lower(), c.get("name", "").lower())
        idx[key] = c

    for character in fetched:
        region = character.get("region")
        realm = character.get("realm")
        name = character.get("name")
        if not all([region, realm, name]):
            continue

        key = (region.lower(), realm.lower(), name.lower())
        dbc = idx.get(key)
        if not dbc:
            continue

        scores = get_nested_dict_or_return_empty(character, CURRENT_SEASON_SCORE)
        new_total = scores.get("scores", {}).get("all", 0)
        if dbc.get("total_rating") == new_total:
            continue

        updated_dungeon_runs = await get_character_updated_dungeon_runs(
            dbc.get("character_id"),
            character.get("mythic_plus_best_runs", []),
            current_season_dungeons,
        )
        character["change"] = {
            "character_id": dbc.get("character_id"),
            "old_rating": dbc.get("total_rating"),
            "new_rating": new_total,
            "updated_dungeon_runs": updated_dungeon_runs,
        }
        output.append(character)

    return output


async def upsert_character_and_runs(changed: List[dict], current_season_dungeons: Dict[str, int]) -> None:
    # Upsert Character and DungeonRun in bulk
    runs: List[DungeonRun] = []
    chars: List[Character] = []

    for character in changed:
        change = character.get("change", {})
        for run in character.get("mythic_plus_best_runs", []):
            runs.append(
                DungeonRun(
                    character_id=change.get("character_id"),
                    dungeon_id=current_season_dungeons.get(run.get("short_name", "").lower()),
                    mythic_level=run.get("mythic_level"),
                    num_keystone_upgrades=run.get("num_keystone_upgrades"),
                    clear_time_ms=run.get("clear_time_ms"),
                    par_time_ms=run.get("par_time_ms"),
                    score=run.get("score"),
                    affix_types=[a.get("name") for a in run.get("affixes", [])],
                )
            )

        scores = get_nested_dict_or_return_empty(character, CURRENT_SEASON_SCORE)
        chars.append(
            Character(
                region=character.get("region", "").lower(),
                realm=character.get("realm", "").lower(),
                name=character.get("name", "").lower(),
                character_class=character.get("class"),
                total_rating=scores.get("scores", {}).get("all", 0),
                dps_rating=scores.get("scores", {}).get("dps", 0),
                healer_rating=scores.get("scores", {}).get("healer", 0),
                tank_rating=scores.get("scores", {}).get("tank", 0),
            )
        )

    if chars:
        await Character.bulk_create(
            chars,
            update_fields=["character_class", "total_rating", "dps_rating", "healer_rating", "tank_rating"],
            on_conflict=["region", "name", "realm"],
        )

    if runs:
        await DungeonRun.bulk_create(
            runs,
            update_fields=["mythic_level", "num_keystone_upgrades", "clear_time_ms", "par_time_ms", "score", "affix_types"],
            on_conflict=["dungeon_id", "character_id"],
        )


async def update_rankings_sql() -> List[dict]:
    """
    Recompute per-server rankings in DB and return changed rows.
    Returns: list of dicts with keys: server_id, character_id, old_ranking, new_ranking
    """
    if not in_transaction:
        return []

    sql = """
    WITH ranked AS (
        SELECT cs.character_id,
               cs.server_id,
               RANK() OVER (PARTITION BY cs.server_id ORDER BY c.total_rating DESC, c.id ASC) AS rk
        FROM character_server cs
        JOIN character c ON c.id = cs.character_id
    ),
    changes AS (
        SELECT cs.character_id,
               cs.server_id,
               cs.ranking       AS old_ranking,
               r.rk             AS new_ranking
        FROM character_server cs
        JOIN ranked r
          ON r.character_id = cs.character_id AND r.server_id = cs.server_id
        WHERE cs.ranking IS DISTINCT FROM r.rk
    )
    UPDATE character_server cs
       SET ranking = ch.new_ranking
      FROM changes ch
     WHERE cs.character_id = ch.character_id
       AND cs.server_id = ch.server_id
    RETURNING cs.server_id, cs.character_id, ch.old_ranking, ch.new_ranking;
    """
    async with in_transaction() as conn:  # type: ignore
        rows, _ = await conn.execute_query(sql)
    return rows or []


def ordinal(n: int) -> str:
    if n % 100 in (11, 12, 13):
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def pluses(n: int) -> str:
    try:
        return "⁺" * max(0, int(n or 0))
    except Exception:
        return ""


def format_run(run: dict) -> str:
    name = run.get("name") or "Unknown"
    clear = run.get("clear_time_ms") or 0
    par = run.get("par_time_ms") or 0
    delta = par - clear
    sign = "Under" if delta > 0 else "Over"
    delta_abs = abs(delta)
    mm = delta_abs // 60000
    ss = (delta_abs // 1000) % 60
    pct = (delta_abs / par * 100) if par > 0 else 0.0
    score = run.get("score") or 0
    level = run.get("mythic_level") or 0
    upgrades = run.get("num_keystone_upgrades") or 0
    return (
        f"- **{name}** {sign} by {mm}:{ss:02d} ({pct:.1f}%), "
        f"Score {score:.1f}, Level {level}{pluses(upgrades)}."
    )


def build_rank_map(rows: List[dict]) -> Dict[int, Dict[int, tuple]]:
    """
    Map: char_id -> server_id -> (old_rank, new_rank)
    Accepts rows as list of dicts or tuples in order.
    """
    mp: Dict[int, Dict[int, tuple]] = {}
    if not rows:
        return mp
    for r in rows:
        if isinstance(r, dict):
            sid = r.get("server_id")
            cid = r.get("character_id")
            old_r = r.get("old_ranking")
            new_r = r.get("new_ranking")
        else:
            # assume tuple/list order: server_id, character_id, old_ranking, new_ranking
            sid, cid, old_r, new_r = r[0], r[1], r[2], r[3]
        if cid is None or sid is None:
            continue
        mp.setdefault(int(cid), {})[int(sid)] = (int(old_r), int(new_r))
    return mp


async def send_change_messages(changed: List[dict], rank_rows: List[dict]) -> None:
    """
    Send messages only for characters that changed.
    Include server ranking delta (rise/drop/stay) and improved dungeon runs.
    """
    # Load server links for characters and current rankings
    server_links = await get_sorted_characters_by_server()
    char_to_servers: Dict[int, List[int]] = {}
    current_rank: Dict[int, Dict[int, int]] = {}
    for link in server_links:
        char_to_servers.setdefault(link.character_id, []).append(link.server_id)
        current_rank.setdefault(link.character_id, {})[link.server_id] = getattr(link, "ranking", None)

    # Map rank deltas from UPDATE RETURNING
    rank_delta = build_rank_map(rank_rows)

    for c in changed:
        ch = c.get("change", {})
        char_id = ch.get("character_id")
        new_rating = ch.get("new_rating") or 0
        old_rating = ch.get("old_rating") or 0
        gain = int(new_rating - old_rating)
        servers = char_to_servers.get(char_id, [])
        if not servers:
            continue

        runs = ch.get("updated_dungeon_runs", [])
        runs_txt = "\n".join(format_run(r) for r in runs) if runs else ""
        for server_id in servers:
            # Determine rank movement
            if char_id in rank_delta and server_id in rank_delta[char_id]:
                old_r, new_r = rank_delta[char_id][server_id]
                verb = "rises at" if new_r < old_r else ("drops to" if new_r > old_r else "stays at")
            else:
                new_r = current_rank.get(char_id, {}).get(server_id)
                verb = "stays at"
            rank_txt = f" {verb} {ordinal(int(new_r))} position." if new_r else ""

            header = (
                f"**{c.get('name')}** +{gain} rating reaching **{int(new_rating)}**{rank_txt}"
            )
            text = f"{header}\n\n{runs_txt}" if runs_txt else header
            await send_to_server(server_id, {"text": text, "character_id": char_id, "server_id": server_id})


async def send_to_server(server_id: int, payload: Dict[str, Any]) -> None:
    """
    Placeholder for your messaging/Discord integration.
    Ensure idempotency if your scheduler can retry.
    """
    # Implement your actual send here.
    print(f"[SEND] server={server_id} payload={payload}")


async def scheduler_beta() -> None:
    """
    Robust, simple batch scheduler:
    - Acquire advisory lock to avoid overlaps
    - Fetch characters and external data
    - Diff changes
    - Bulk upsert Character and DungeonRun
    - Recompute rankings in SQL (atomic)
    - Send messages only for changed characters
    """
    if not in_transaction:
        # Fall back without advisory lock if no transaction manager is present
        await _scheduler_beta_no_lock()
        return

    # Hold the lock connection open for the duration of the run
    async with in_transaction() as lock_conn:  # type: ignore
        rows, _ = await lock_conn.execute_query("SELECT pg_try_advisory_lock($1);", [ADVISORY_LOCK_KEY])
        acquired = bool(rows and rows[0] and (rows[0][0] if isinstance(rows[0], (list, tuple)) else list(rows[0].values())[0]))

        if not acquired:
            print("scheduler_beta: another run is in progress; exiting")
            return

        try:
            await _scheduler_beta_no_lock()
        finally:
            await lock_conn.execute_query("SELECT pg_advisory_unlock($1);", [ADVISORY_LOCK_KEY])


async def _scheduler_beta_no_lock() -> None:
    current_season_dungeons = await get_current_season_dungeons()

    db_chars = [
        {
            "region": c.region,
            "realm": c.realm,
            "name": c.name,
            "character_id": c.id,
            "total_rating": c.total_rating,
        }
        for c in await get_all_characters()
    ]

    fetched = await get_multiple_wow_characters(db_chars)
    changed = await add_score_differs_to_characters(fetched, db_chars, current_season_dungeons)

    if not changed:
        print("scheduler_beta: no changes")
        return

    await upsert_character_and_runs(changed, current_season_dungeons)
    rank_rows = await update_rankings_sql()
    await send_change_messages(changed, rank_rows)
