from settings import (
    WOW_API_URL,
    ALTERNATIVE_RUN_FIELDS,
    BEST_RUN_FIELDS,
    CURRENT_SEASON_SCORE,
    RAID_PROGRESSION,
    GEAR,
    MYTHIC_PLUS_RECENT_RUNS,
)


def generate_api_url_for_char_fetch(character: dict) -> str:
    return f'{WOW_API_URL}/characters/profile?region={character["region"]}&realm={character["realm"]}&name={character["name"]}&fields={ALTERNATIVE_RUN_FIELDS},{BEST_RUN_FIELDS},{CURRENT_SEASON_SCORE}'


def generate_api_url_for_char_fetch_check(character: dict) -> str:
    return f'{WOW_API_URL}/characters/profile?region={character["region"]}&realm={character["realm"]}&name={character["name"]}&fields={CURRENT_SEASON_SCORE},{RAID_PROGRESSION},{GEAR},{MYTHIC_PLUS_RECENT_RUNS}'
