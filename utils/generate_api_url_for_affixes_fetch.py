from settings import WOW_API_URL


def generate_api_url_for_affixes_fetch(region: str) -> str:
    return f"{WOW_API_URL}/mythic-plus/affixes?region={region}&locale=en"
