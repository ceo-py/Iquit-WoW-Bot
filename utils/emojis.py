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
    affixes_emojis = {
        affix.name: affix.icon_discord for affix in await get_all_emojis(type)
    }
    return affixes_emojis
