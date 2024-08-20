import asyncio
import aiohttp
from utils.generate_api_url_for_char_fetch import generate_api_url_for_char_fetch
from typing import List


async def fetch(session: aiohttp.ClientSession, url: str) -> "json":
    async with session.get(url) as response:
        return await response.json()


async def get_wow_character(character: dict) -> "json":
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, generate_api_url_for_char_fetch(character))
        return response


async def get_multiple_wow_characters(characters: list) -> List["json"]:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for character in characters:
            tasks.append(fetch(session, generate_api_url_for_char_fetch(character)))
        responses = await asyncio.gather(*tasks)
        return responses
