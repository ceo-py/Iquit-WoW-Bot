from database.service.emojis_discord_service import get_all_emojis
from typing import Dict


async def get_emojis(type: str) -> Dict[str, str]:
    """
    Current types of Emojis:
    - Affix
    - Character
    - Common
    - Dungeon
    - Region
    - Character_Role
    """
    emojis = {emoji.name: emoji.icon_discord for emoji in await get_all_emojis(type)}
    return emojis
