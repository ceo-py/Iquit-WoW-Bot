from settings import (
    WOW_API_URL,
    ALTERNATIVE_RUN_FIELDS,
    BEST_RUN_FIELDS,
    CURRENT_SEASON_SCORE,
    RAID_PROGRESSION,
    GEAR,
    MYTHIC_PLUS_RECENT_RUNS,
)


def base_url(character: dict):
    return f'{WOW_API_URL}/characters/profile?region={character["region"]}&realm={character["realm"]}&name={character["name"]}&fields='


def generate_api_url_for_char_fetch(character: dict) -> str:
    url = base_url(character)
    return f"{url}{ALTERNATIVE_RUN_FIELDS},{BEST_RUN_FIELDS},{CURRENT_SEASON_SCORE}:current"


def generate_api_url_for_char_fetch_check(character: dict) -> str:
    url = base_url(character)
    return f"{url}{CURRENT_SEASON_SCORE},{RAID_PROGRESSION},{GEAR},{MYTHIC_PLUS_RECENT_RUNS}"
