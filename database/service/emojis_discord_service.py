from database.models.emojis_discord import (
    AffixDiscordIcons,
    CharacterDiscordIcons,
    CommonDiscordIcons,
    DungeonDiscordIcons,
    RegionDiscordIcons,
    CharacterRoleDiscordIcons,
    BaseEmojiDiscord,
)
from typing import List

TYPES = {
    "Affix": AffixDiscordIcons,
    "Character": CharacterDiscordIcons,
    "Common": CommonDiscordIcons,
    "Dungeon": DungeonDiscordIcons,
    "Region": RegionDiscordIcons,
    "Character_Role": CharacterRoleDiscordIcons,
}


async def get_emoji_by_name(name: str, type: str) -> BaseEmojiDiscord:
    """
    Retrieve a Emoji instance by its name with given emoji type.

    This asynchronous function fetches a Emoji record from the database
    using the provided Emoji name and type. If no record is found, it returns None.

    Parameters:
    -----------
    name : str
        The name of the Emoji record to be retrieved.

    type : str
        The name of the Type Emoji record to be retrieved.
            Options: "Affix", "Character", "Common", "Dungeon", "Region", "Character_Role",

    Returns:
    --------
    Emoji or None
        The Emoji instance if found, otherwise None.
    """
    emoji = await TYPES.get(type).get_or_none(name=name)
    return emoji


async def create_emoji(name: str, icon_discord: str, type: str) -> BaseEmojiDiscord:
    """
    Create a new Emoji instance and save it to the database.

    This asynchronous function creates a new Emoji record in the database using the
    provided parameters and returns the newly created Emoji instance.

    Parameters:
    -----------
    name : str
        The name of the Emoji.
    icon_discord : str
        The Text for the Emoji's icon on Discord.
        Example  => <:Ascendant:1267593476678352980>

    type : str
        The name of the Type Emoji record to be retrieved.
            Options: "Affix", "Character", "Common", "Dungeon", "Region", "Character_Role",

    Returns:
    --------
    None
    """
    await TYPES.get(type).create(
        name=name,
        icon_discord=icon_discord,
    )


async def get_all_emojis(type: str) -> List[BaseEmojiDiscord]:
    """
    Retrieve all Emoji instances from the database base on type.

    This asynchronous function fetches all Emoji records from the database
    and returns them as a list.

    Parameters:
    -----------
    type : str
        The name of the Type Emoji record to be retrieved.
            Options: "Affix", "Character", "Common", "Dungeon", "Region", "Character_Role",

    Returns:
    --------
    List[Emoji]
        A list containing all Emoji instances in the database.
    """

    return await TYPES.get(type).all()
