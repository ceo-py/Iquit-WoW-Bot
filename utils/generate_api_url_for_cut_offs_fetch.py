from settings import WOW_API_URL


def generate_api_url_for_cut_offs_fetch(
    region: str, season_name: str, season_number: int
) -> str:
    """
    https://raider.io/api/v1/mythic-plus/season-cutoffs?season=season-tww-1&region=eu
    """
    return f"{WOW_API_URL}/mythic-plus/season-cutoffs?season=season-{season_name}-{season_number}&region={region}"
