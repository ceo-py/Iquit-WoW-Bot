import aiohttp
from utils.api.generate_api_url_for_affixes_fetch import (
    generate_api_url_for_affixes_fetch,
)
from .request_character_information import fetch


async def get_wow_affixes(region: str) -> str:
    async with aiohttp.ClientSession() as session:
        response = await fetch(
            session,
            generate_api_url_for_affixes_fetch(region),
        )
        return response.get("title")
