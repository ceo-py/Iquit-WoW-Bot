from settings import WOW_API_URL


def generate_api_url_for_cut_offs_fetch(
    region: str, season_name: str, season_number: int
) -> str:
    return f"{WOW_API_URL}/mythic-plus/season-cutoffs?season=season-{season_name}-{season_number}&region={region}"
