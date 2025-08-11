from database.service.character_service import get_all_characters
from database.service.character_server_service import get_sorted_characters_by_server
from database.service.dungeon_service import get_all_current_season_dungeons
from database.service.dungeon_run_service import get_all_dungeon_runs_for_character
from database.models.dungeon_run import DungeonRun
from database.models.character import Character
from database.models.character_server import CharacterServer
from utils.api.request_character_information import get_multiple_wow_characters
from utils import get_nested_dict_or_return_empty
from settings import CURRENT_SEASON_SCORE


async def get_current_season_dungeons():
    return {
        dungeon.short_name.lower(): dungeon.id
        for dungeon in await get_all_current_season_dungeons()
    }


async def update_character_rating(characters: list) -> list:
    discord_server_characters = await get_sorted_characters_by_server()
    current_servers = {}  # {"id discord server": [discord_character]}
    updated_characters = {}  # {"id character": character}

    for discord_character in discord_server_characters:
        current_servers[discord_character.server_id] = current_servers.get(
            discord_character.server_id, []
        ) + [discord_character]

    for update_character in characters:
        updated_characters[update_character.get("change").get("character_id")] = (
            update_character
        )

    for server_id, characters_in_server in current_servers.items():
        found_characters = []

        for discord_character in characters_in_server:
            found_character = updated_characters.get(discord_character.character_id)
            character_id = (
                found_character.get("change").get("character_id")
                if found_character
                else discord_character.character_id
            )
            character_rating = (
                found_character.get("change").get("new_rating")
                if found_character
                else discord_character.character.total_rating
            )
            found_characters.append(
                {
                    "character": character_id,
                    "server": server_id,
                    "rating": character_rating,
                }
            )

        old_ratings = sorted(
            characters_in_server, key=lambda x: -x.character.total_rating
        )
        new_ratings = sorted(found_characters, key=lambda x: -x.get("rating"))

        print(f"old_ratings: {old_ratings}\nnew_ratings: {new_ratings}")

        # print(
        #     f"{discord_character.character_id} {discord_character.server_id} {discord_character.ranking} => {discord_character.character.total_rating}"
        # )

    # output = []
    # characters_update = []

    # for discord_character in discord_server_characters:
    #     for character in characters:
    #         character_id = character.get("change").get("character_id")
    #         if discord_character.character != character_id:
    #             continue

    #         characters_update.append(
    #             CharacterServer(
    #                 character=character_id,
    #                 server=discord_character.server,
    #                 ranking=0,
    #             )
    #         )

    # await CharacterServer.bulk_create(
    #     characters_update,
    #     update_fields=[
    #         "ranking",
    #     ],
    #     on_conflict=["character", "server"],
    # )

    # return output


async def update_dungeon_runs(characters: dict, current_season_dungeons: dict) -> None:
    dungeon_runs = []
    updated_character_ratings = []
    for character in characters:
        for run in character.get("mythic_plus_best_runs", []):
            dungeon_runs.append(
                DungeonRun(
                    character_id=character.get("change", {}).get("character_id"),
                    dungeon_id=current_season_dungeons.get(
                        run.get("short_name").lower()
                    ),
                    mythic_level=run.get("mythic_level"),
                    num_keystone_upgrades=run.get("num_keystone_upgrades"),
                    clear_time_ms=run.get("clear_time_ms"),
                    par_time_ms=run.get("par_time_ms"),
                    score=run.get("score"),
                    affix_types=[
                        affix.get("name") for affix in run.get("affixes", [{}])
                    ],
                )
            )
            scores_by_season = get_nested_dict_or_return_empty(
                character, CURRENT_SEASON_SCORE
            )
            updated_character_ratings.append(
                Character(
                    region=character.get("region").lower(),
                    realm=character.get("realm").lower(),
                    name=character.get("name").lower(),
                    character_class=character.get("class"),
                    total_rating=character.get(scores_by_season)
                    .get("scores", {})
                    .get("all", 0),
                    dps_rating=character.get(scores_by_season)
                    .get("scores", {})
                    .get("dps", 0),
                    healer_rating=character.get(scores_by_season)
                    .get("scores", {})
                    .get("healer", 0),
                    tank_rating=character.get(scores_by_season)
                    .get("scores", {})
                    .get("tank", 0),
                )
            )

    await Character.bulk_create(
        updated_character_ratings,
        update_fields=[
            "character_class",
            "total_rating",
            "dps_rating",
            "healer_rating",
            "tank_rating",
        ],
        on_conflict=["region", "name", "realm"],
    )

    await DungeonRun.bulk_create(
        dungeon_runs,
        update_fields=[
            "mythic_level",
            "num_keystone_upgrades",
            "clear_time_ms",
            "par_time_ms",
            "score",
            "affix_types",
        ],
        on_conflict=["dungeon_id", "character_id"],
    )


def add_dungeon_details(new_score: int, new_run: dict, updated_runs: list) -> list:
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
    return updated_runs


async def get_character_updated_dungeon_runs(
    character_id: int, updated_dungeon_runs: list, current_season_dungeons: dict
) -> list:
    updated_runs = []
    db_runs = await get_all_dungeon_runs_for_character(character_id)

    if not db_runs:
        for run in updated_dungeon_runs:
            score = run.get("score", 0)
            if score > 0:
                add_dungeon_details(score, run, updated_runs)
        return updated_runs

    for db_run in db_runs:
        remaining_runs = []
        for new_run in updated_dungeon_runs:
            score = new_run.get("score", 0)
            if score == 0:
                continue

            dungeon_id = current_season_dungeons.get(new_run.get("short_name").lower())
            if db_run.dungeon_id == dungeon_id:
                if score > db_run.score:
                    add_dungeon_details(score, new_run, updated_runs)
            else:
                remaining_runs.append(new_run)
        updated_dungeon_runs = remaining_runs

    for run in updated_dungeon_runs:
        score = run.get("score", 0)
        if score > 0:
            add_dungeon_details(score, run, updated_runs)

    return updated_runs


async def add_score_differs_to_characters(
    fetch_characters: list, db_characters: list, current_season_dungeons: dict
) -> list:
    output = []
    for character in fetch_characters:
        fetch_character_data = (
            character.get("name"),
            character.get("realm"),
            character.get("region"),
        )
        if any(c is None for c in fetch_character_data):
            continue
        fetch_character = set(x.lower() for x in fetch_character_data)

        for index, db_character in enumerate(db_characters):
            db_character_data = (
                db_character.get("name"),
                db_character.get("realm"),
                db_character.get("region"),
            )
            if any(c is None for c in db_character_data):
                db_characters.pop(index)
                continue

            current_score = get_nested_dict_or_return_empty(character, CURRENT_SEASON_SCORE)
            current_character_score = (
                character.get(current_score)
                .get("scores", {})
                .get("all", 0)
            )
            if (
                fetch_character.difference(set(x.lower() for x in db_character_data))
                or db_character.get("total_rating") == current_character_score
            ):
                continue
            updated_dungeon_runs = await get_character_updated_dungeon_runs(
                db_character.get("character_id"),
                character.get("mythic_plus_best_runs", []),
                current_season_dungeons,
            )
            character["change"] = {
                "character_id": db_character.get("character_id"),
                "old_rating": db_character.get("total_rating"),
                "new_rating": current_character_score,
                "updated_dungeon_runs": updated_dungeon_runs,
            }
            output.append(character)
            db_characters.pop(index)
            break

    return output


async def task_scheduler():
    current_season_dungeons = await get_current_season_dungeons()
    all_characters_in_db = [
        {
            "region": c.region,
            "realm": c.realm,
            "name": c.name,
            "character_id": c.id,
            "total_rating": c.total_rating,
        }
        for c in await get_all_characters()
    ]
    characters_update_data = await get_multiple_wow_characters(all_characters_in_db)
    characters = await add_score_differs_to_characters(
        characters_update_data, all_characters_in_db, current_season_dungeons
    )
    [print(c["change"]) for c in characters]
    await update_dungeon_runs(characters, current_season_dungeons)
    await update_character_rating(characters)
