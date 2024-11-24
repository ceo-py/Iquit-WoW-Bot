from database.service.character_service import get_all_characters
from database.service.dungeon_service import get_all_dungeons
from database.service.dungeon_run_service import update_or_create_dungeon_run
from database.models.dungeon_run import DungeonRun
from database.models.character import Character
from utils.api.request_character_information import get_multiple_wow_characters


async def get_current_season_dungeons():
    return {
        dungeon.short_name.lower(): dungeon.id for dungeon in await get_all_dungeons()
    }


async def update_dungeon_runs(characters: dict, current_season_dungeons: dict):
    dungeon_runs = []
    updated_character_ratings = []
    for character in characters:
        for run in character.get("mythic_plus_best_runs", []):
            dungeon_runs.append(
                DungeonRun(
                    character_id=character.get("character_id"),
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

            updated_character_ratings.append(
                Character(
                    region=character.get("region").lower(),
                    realm=character.get("realm").lower(),
                    name=character.get("name").lower(),
                    character_class=character.get("class"),
                    total_rating=character.get("mythic_plus_scores_by_season", [{}])[0]
                    .get("scores", {})
                    .get("all", 0),
                    dps_rating=character.get("mythic_plus_scores_by_season", [{}])[0]
                    .get("scores", {})
                    .get("dps", 0),
                    healer_rating=character.get("mythic_plus_scores_by_season", [{}])[0]
                    .get("scores", {})
                    .get("healer", 0),
                    tank_rating=character.get("mythic_plus_scores_by_season", [{}])[0]
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


def add_character_id_when_score_differs(
    fetch_characters: list, db_characters: list
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
            current_character_score = (
                character.get("mythic_plus_scores_by_season", [{}])[0]
                .get("scores", {})
                .get("all", 0)
            )
            if (
                fetch_character.difference(set(x.lower() for x in db_character_data))
                and db_character.get("total_rating") == current_character_score
            ):
                continue
            character["character_id"] = db_character.get("character_id")
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
    characters = add_character_id_when_score_differs(
        characters_update_data, all_characters_in_db
    )
    await update_dungeon_runs(characters, current_season_dungeons)
