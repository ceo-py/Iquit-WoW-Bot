from database.service.character_service import get_all_characters
from database.service.dungeon_service import get_all_dungeons
from database.service.dungeon_run_service import update_or_create_dungeon_run
from utils.api.request_character_information import get_multiple_wow_characters


async def get_current_season_dungeons():
    return {
        dungeon.short_name.lower(): dungeon.id for dungeon in await get_all_dungeons()
    }


async def update_dungeon_run(
    dungeon_run: dict, character_id: int, current_season_dungeons: dict
):
    data = {
        "character_id": character_id,
        "dungeon_id": current_season_dungeons.get(
            dungeon_run.get("short_name").lower()
        ),
        "mythic_level": dungeon_run.get("mythic_level"),
        "num_keystone_upgrades": dungeon_run.get("num_keystone_upgrades"),
        "clear_time_ms": dungeon_run.get("clear_time_ms"),
        "par_time_ms": dungeon_run.get("par_time_ms"),
        "score": dungeon_run.get("score"),
        "affix_types": [
            affix.get("name") for affix in dungeon_run.get("affixes", [{}])
        ],
    }
    await update_or_create_dungeon_run(**data)


def add_character_id_when_score_differs(fetch_characters: list, db_characters: list) -> list:
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
    characters = add_character_id_when_score_differs(characters_update_data, all_characters_in_db)
    for character in characters:
        dungeon_runs = character.get("mythic_plus_best_runs", [])
        if not dungeon_runs:
            continue
        for dungeon_run in dungeon_runs:
            await update_dungeon_run(
                dungeon_run, character.get("character_id"), current_season_dungeons
            )
            break
