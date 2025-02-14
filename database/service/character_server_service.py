from database.models.character_server import CharacterServer
from typing import List


async def create_character_server(
    character_id: int, server_id: int, ranking: int
) -> CharacterServer:
    """
    Create a new CharacterServer instance and save it to the database.

    This function creates a new CharacterServer record in the database using the
    provided parameters.

    Parameters:
    -----------
    character_id : int
        The ID of the character associated with this server record.
    server_id : int
        The ID of the server where the character is located.
    ranking : int
        The ranking of the character on this server.

    Returns:
    --------
    CharacterServer
        The newly created CharacterServer instance.
    """
    character_server = await CharacterServer.create(
        character_id=character_id, server_id=server_id, ranking=ranking
    )
    return character_server


async def get_character_by_id_with_server_id(
    character_id: int, server_id: int
) -> CharacterServer:
    """
    Retrieve a CharacterServer instance by its ID.

    This asynchronous function fetches a CharacterServer record from the database
    using the provided character_id and server_id. If no record is found, it returns None.

    Parameters:
    -----------
    character_id : int
        The ID of the Character record to be retrieved.

    Returns:
    --------
    CharacterServer or None
        The CharacterServer instance if found, otherwise None.
    """
    character_server = await CharacterServer.get_or_none(
        character_id=character_id, server_id=server_id
    )
    return character_server


async def get_all_characters_from_discord_server_by_id(
    server_id: int,
) -> List[CharacterServer]:
    """
    Retrieve all CharacterServer instances for a given server ID.

    This asynchronous function fetches all CharacterServer records from the database
    that match the provided server_id.

    Parameters:
    -----------
    server_id : int
        The ID of the Discord server to retrieve characters for.

    Returns:
    --------
    List[CharacterServer]
        A list of CharacterServer instances associated with the given server_id.
    """
    character_servers = await CharacterServer.filter(server_id=server_id)
    return character_servers


async def get_character_by_id(character_id: int) -> CharacterServer:
    """
    Retrieve a CharacterServer instance by its ID.

    This asynchronous function fetches a CharacterServer record from the database
    using the provided character_id. If no record is found, it returns None.

    Parameters:
    -----------
    character_id : int
        The ID of the Character record to be retrieved.

    Returns:
    --------
    CharacterServer or None
        The CharacterServer instance if found, otherwise None.
    """
    character_server = await CharacterServer.get_or_none(character_id=character_id)
    return character_server


async def update_character_server_ranking(
    character_server_id: int, ranking: int
) -> CharacterServer:
    """
    Update the ranking of a CharacterServer instance.

    This asynchronous function updates the ranking of a CharacterServer record in the database
    using the provided character_server_id and ranking. It does not return any value.

    Parameters:
    -----------
    character_server_id : int
        The ID of the CharacterServer record to be updated.
    ranking : int
        The new ranking to be assigned to the CharacterServer.

    Returns:
    --------
    None
    """
    await CharacterServer.filter(id=character_server_id).update(ranking=ranking)


async def delete_character_from_server(
    character_id: int, server_id: int
) -> CharacterServer:
    """
    Delete a CharacterServer instance by its ID.

    This asynchronous function deletes a CharacterServer record from the database
    using the provided character_id and server_id. It does not return any value.

    Parameters:
    -----------
    character_id : int
        The ID of the Character record to be deleted.
    server_id : int
        The unique identifier of the server from which the character should be removed.

    Returns:
    --------
    None
    """
    await CharacterServer.filter(
        character_id=character_id, server_id=server_id
    ).delete()


async def get_sorted_characters_by_server():
    """
    Get sorted characters by server.

    Returns:
    --------
    List[CharacterServer]
        A list of CharacterServer instances sorted by server and total_rating.
    """
    character_servers = (
        await CharacterServer.all()
        .select_related("character", "server")
        .order_by("server__id", "-character__total_rating")
    )

    return character_servers

async def reset_all_character_server_rankings() -> int:
    """
    Resets all character ranking in discord servers to 0.
    
    Returns:
        int: Number of characters updated
    """
    updated = await CharacterServer.all().update(
        ranking=0,
    )
    return updated