import aiohttp
from utils.api.generate_api_url_for_cut_offs_fetch import (
    generate_api_url_for_cut_offs_fetch,
)
from api.request_character_information import fetch


async def get_wow_cut_offs(region: str, season_name: str, season_number: int) -> "json":
    async with aiohttp.ClientSession() as session:
        response = await fetch(
            session,
            generate_api_url_for_cut_offs_fetch(region, season_name, season_number),
        )
        return response
