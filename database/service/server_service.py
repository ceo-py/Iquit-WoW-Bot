from database.models.server import Server
from database.models.dungeon_run import DungeonRun


async def create_server(discord_server_id: int) -> Server:
    """
    Create a new Server instance in the database.

    This function creates a new Server record in the database with the given
    Discord server ID.

    Parameters:
    -----------
    discord_server_id : int
        The unique identifier of the Discord server.

    discord_channel_id : int
        The unique identifier of the Discord channel.

    Returns:
    --------
    Server
        The newly created Server instance.

    """
    server = await Server.create(discord_server_id=discord_server_id)
    return server


async def create_or_get_server(discord_server_id: int) -> Server:
    """
    Get an existing Server instance or create a new one if it doesn't exist.

    This function attempts to retrieve a Server record from the database using the given
    Discord server ID. If no record exists, it creates a new one.

    Parameters:
    -----------
    discord_server_id : int
        The unique identifier of the Discord server.

    Returns:
    --------
    Server
        The existing or newly created Server instance.

    """
    server = await Server.get_or_create(discord_server_id=discord_server_id)
    return server


async def get_server_by_id(server_id: int) -> Server:
    """
    Retrieve a Server instance from the database by its ID.

    This function fetches a Server record from the database using the given
    server ID.

    Parameters:
    -----------
    server_id : int
        The unique identifier of the server in the database.

    Returns:
    --------
    Server
        The Server instance if found, or None if not found.

    """
    server = await Server.get_or_none(id=server_id)
    return server


async def get_server_by_discord_id(discord_server_id: int) -> Server:
    """
    Retrieve a Server instance from the database by its Discord server ID.

    This function fetches a Server record from the database using the given
    Discord server ID.

    Parameters:
    -----------
    discord_server_id : int
        The unique identifier of the Discord server.

    Returns:
    --------
    Server
        The Server instance if found, or None if not found.

    """
    server = await Server.get_or_none(discord_server_id=discord_server_id)
    return server


async def update_server(discord_server_id: int, discord_channel_id: int) -> None:
    """
    Update the Discord channel ID for an existing Server instance.

    This function updates the Discord channel ID of a Server record in the
    database identified by the given Discord server ID.

    Parameters:
    -----------
    discord_server_id : int
        The Discord server ID used to identify the server record.
    discord_channel_id : int
        The new Discord channel ID to be updated.

    Returns:
    --------
    None

    """
    await Server.filter(discord_server_id=discord_server_id).update(
        discord_channel_id=discord_channel_id
    )


async def delete_server(server_id: int) -> None:
    """
    Delete a Server instance and its associated data from the database.

    This function removes a Server record and its related data from the
    database using the given server ID.

    Parameters:
    -----------
    server_id : int
        The unique identifier of the server in the database.

    Returns:
    --------
    None

    """
    await delete_server_and_associated_data(server_id)


async def delete_server_and_associated_data(server_id: int):
    """
    Delete a Server instance and its associated data, including characters.

    This function removes a Server record, its related characters, and their
    associated dungeon runs from the database using the given server ID.

    Parameters:
    -----------
    server_id : int
        The unique identifier of the server in the database.

    Returns:
    --------
    None

    """
    server = await get_server_by_discord_id(server_id)
    if server:
        characters = await server.characters.all()
        await server.delete()
        for character in characters:
            remaining_servers = await character.servers.all()
            if not remaining_servers:
                # Delete associated DungeonRun records
                await DungeonRun.filter(character=character).delete()
                # Delete the character
                await character.delete()
