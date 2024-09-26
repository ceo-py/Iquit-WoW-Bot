from database.models.dungeon import Dungeon


async def get_dungeon_by_short_name(short_name: str) -> Dungeon:
    """
    Retrieve a Dungeon instance by its short name.

    This asynchronous function fetches a Dungeon record from the database
    using the provided short_name. If no record is found, it returns None.

    Parameters:
    -----------
    short_name : str
        The short name of the Dungeon record to be retrieved.

    Returns:
    --------
    Dungeon or None
        The Dungeon instance if found, otherwise None.
    """
    dungeon = await Dungeon.get_or_none(short_name=short_name)
    return dungeon


async def get_all_dungeons() -> list[Dungeon]:
    """
    Retrieve all Dungeon instances.

    This asynchronous function fetches all Dungeon records from the database.

    Returns:
    --------
    list[Dungeon]
        A list of all Dungeon instances.
    """
    dungeons = await Dungeon.all()
    return dungeons


async def create_dungeon(name: str, short_name: str, icon_discord: str) -> Dungeon:
    """
    Create a new Dungeon instance and save it to the database.

    This asynchronous function creates a new Dungeon record in the database using the
    provided parameters and returns the newly created Dungeon instance.

    Parameters:
    -----------
    name : str
        The name of the dungeon.
    short_name : str
        The short name of the dungeon.
    icon_discord : str
        The Text for the dungeon's icon on Discord.
        Example  => <:aa:1239630623262511135>

    Returns:
    --------
    Dungeon
        The newly created Dungeon instance.
    """
    dungeon = await Dungeon.create(
        name=name,
        short_name=short_name,
        icon_discord=icon_discord,
    )
    return dungeon
