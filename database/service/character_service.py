from database.models.character import Character
from typing import List


async def create_character(
    region: str,
    realm: str,
    name: str,
    character_class: str,
    total_rating: int,
    dps_rating: int,
    healer_rating: int,
    tank_rating: int,
) -> Character:
    """
    Create a new Character instance and save it to the database.

    This asynchronous function creates a new Character record in the database using the
    provided parameters and returns the newly created Character instance.

    Parameters:
    -----------
    region : str
        The region where the character is located.
    realm : str
        The realm where the character is located.
    name : str
        The name of the character.
    character_class : str
        The class of the character (e.g., Warrior, Mage).
    total_rating : int
        The total rating of the character.
    dps_rating : int
        The DPS (Damage Per Second) rating of the character.
    healer_rating : int
        The healing rating of the character.
    tank_rating : int
        The tanking rating of the character.

    Returns:
    --------
    Character
        The newly created Character instance.
    """
    character = await Character.create(
        region=region,
        realm=realm,
        name=name,
        character_class=character_class,
        total_rating=total_rating,
        dps_rating=dps_rating,
        healer_rating=healer_rating,
        tank_rating=tank_rating,
    )
    return character


async def get_character_by_id(character_id: int) -> Character:
    """
    Retrieve a Character instance by its ID.

    This asynchronous function fetches a Character record from the database
    using the provided character_id. If no record is found, it returns None.

    Parameters:
    -----------
    character_id : int
        The ID of the Character record to be retrieved.

    Returns:
    --------
    Character or None
        The Character instance if found, otherwise None.
    """
    character = await Character.get_or_none(id=character_id)
    return character


async def get_characters_by_ids(character_ids: List[int]) -> List[Character]:
    """
    Retrieve multiple Character instances by their IDs.

    This asynchronous function fetches multiple Character records from the database
    using the provided list of character_ids. It returns a list of Character instances
    for all the IDs that were found in the database.

    Parameters:
    -----------
    character_ids : List[int]
        A list of Character IDs to be retrieved.

    Returns:
    --------
    List[Character]
        A list of Character instances corresponding to the provided IDs.
        If an ID is not found, it will not be included in the result.
    """
    characters = await Character.filter(id__in=character_ids)
    return characters


async def get_character_by_region_realm_name(
    region: str, realm: str, name: str
) -> Character:
    """
    Retrieve a Character instance by its region, realm, and name.

    This asynchronous function fetches a Character record from the database
    using the provided region, realm, and name. If no record is found, it returns None.

    Parameters:
    -----------
    region : str
        The region where the character is located.
    realm : str
        The realm where the character is located.
    name : str
        The name of the character.

    Returns:
    --------
    Character or None
        The Character instance if found, otherwise None.
    """
    character = await Character.get_or_none(region=region, realm=realm, name=name)
    return character


async def update_character(character_id: int, **kwargs: dict) -> None:
    """
    Update a Character instance with the given parameters.

    This asynchronous function updates a Character record in the database
    using the provided character_id and keyword arguments. The keyword arguments
    specify the fields to be updated and their new values. It does not return any value.

    Parameters:
    -----------
    character_id : int
        The ID of the Character record to be updated.
    **kwargs : dict
        A dictionary of fields and their new values to update in the Character record.
        The possible fields are:

        - region (str): Region where the character is located, with a maximum length of 50 characters.
        - realm (str): Realm where the character is located, with a maximum length of 50 characters.
        - name (str): Name of the character, with a maximum length of 100 characters.
        - character_class (str): Class of the character, with a maximum length of 50 characters.
        - total_rating (float): Total rating of the character.
        - dps_rating (float): DPS (Damage Per Second) rating of the character.
        - healer_rating (float): Healer rating of the character.
        - tank_rating (float): Tank rating of the character.

    Returns:
    --------
    None
    """
    await Character.filter(id=character_id).update(**kwargs)


async def delete_character(character_id: int) -> None:
    """
    Delete a Character instance by its ID.

    This asynchronous function deletes a Character record from the database
    using the provided character_id. It does not return any value.

    Parameters:
    -----------
    character_id : int
        The ID of the Character record to be deleted.

    Returns:
    --------
    None
    """
    await Character.filter(id=character_id).delete()


async def get_all_characters() -> List[Character]:
    """
    Retrieve all Character instances from the database.
    """
    characters = await Character.all()
    return characters


async def reset_all_character_ratings() -> int:
    """
    Resets all character ratings to 0.

    Returns:
        int: Number of characters updated
    """
    updated = await Character.all().update(
        tank_rating=0, healer_rating=0, dps_rating=0, total_rating=0
    )
    return updated
