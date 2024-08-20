import asyncio
import aiohttp
from settings import WOW_API_URL, ALTERNATIVE_RUN_FIELDS, BEST_RUN_FIELDS


async def fetch(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        return await response.json()


async def get_wow_character(character: dict):
    async with aiohttp.ClientSession() as session:
        url = f'{WOW_API_URL}/characters/profile?region={character["region"]}&realm={character["realm"]}&name={character["name"]}&fields={ALTERNATIVE_RUN_FIELDS},{BEST_RUN_FIELDS}'
        response = await fetch(session, url)
        return response


async def get_multiple_wow_characters(characters: list):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for character in characters:
            url = f'{WOW_API_URL}/characters/profile?region={character["region"]}&realm={character["realm"]}&name={character["name"]}&fields={ALTERNATIVE_RUN_FIELDS},{BEST_RUN_FIELDS}'
            tasks.append(fetch(session, url))
        responses = await asyncio.gather(*tasks)
        return responses


