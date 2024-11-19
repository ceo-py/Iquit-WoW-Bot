import asyncio
import aiohttp
from utils.generate_api_url_for_char_fetch import (
    generate_api_url_for_char_fetch,
    generate_api_url_for_char_fetch_check,
)
from .rate_limiter import rate_limiter
from typing import List


async def fetch(session: aiohttp.ClientSession, url: str) -> "json":
    async with session.get(url) as response:
        await rate_limiter.wait_for_token()
        return await response.json()


async def get_wow_character(character: dict) -> "json":
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, generate_api_url_for_char_fetch(character))
        return response


async def get_wow_character_check(character: dict) -> "json":
    async with aiohttp.ClientSession() as session:
        response = await fetch(
            session, generate_api_url_for_char_fetch_check(character)
        )
        return response


async def get_multiple_wow_characters(characters: list) -> List["json"]:
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(
                fetch(session, generate_api_url_for_char_fetch(character))
            )
            for character in characters
        ]
        responses = await asyncio.gather(*tasks)

        return responses
