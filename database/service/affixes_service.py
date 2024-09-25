from database.models.affixes import Affixes


async def get_affix_by_name(name: str) -> Affixes:
    """
    Retrieve a Affix instance by its name.

    This asynchronous function fetches a Affix record from the database
    using the provided affix name. If no record is found, it returns None.

    Parameters:
    -----------
    name : str
        The name of the Affix record to be retrieved.

    Returns:
    --------
    Affix or None
        The Affix instance if found, otherwise None.
    """
    affix = await Affixes.get_or_none(name=name)
    return affix


async def create_affix(name: str, icon_discord: str) -> Affixes:
    """
    Create a new Affix instance and save it to the database.

    This asynchronous function creates a new affix record in the database using the
    provided parameters and returns the newly created affix instance.

    Parameters:
    -----------
    name : str
        The name of the affix.
    icon_discord : str
        The Text for the affix's icon on Discord.
        Example  => <:Ascendant:1267593476678352980>

    Returns:
    --------
    Affix
        The newly created Affix instance.
    """
    dungeon = await Affixes.create(
        name=name,
        icon_discord=icon_discord,
    )
    return dungeon
