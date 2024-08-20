from database.models.character_server import CharacterServer


async def create_character_server(character_id: int, server_id: int, ranking: int) -> CharacterServer:
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
        character_id=character_id,
        server_id=server_id,
        ranking=ranking
    )
    return character_server


async def get_character_server_by_id(character_server_id: int) -> CharacterServer:
    """
    Retrieve a CharacterServer instance by its ID.

    This asynchronous function fetches a CharacterServer record from the database
    using the provided character_server_id. If no record is found, it returns None.

    Parameters:
    -----------
    character_server_id : int
        The ID of the CharacterServer record to be retrieved.

    Returns:
    --------
    CharacterServer or None
        The CharacterServer instance if found, otherwise None.
    """
    character_server = await CharacterServer.get_or_none(id=character_server_id)
    return character_server


async def update_character_server_ranking(character_server_id: int, ranking: int) -> CharacterServer:
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


async def delete_character_server(character_server_id: int) -> CharacterServer:
    """
    Delete a CharacterServer instance by its ID.

    This asynchronous function deletes a CharacterServer record from the database
    using the provided character_server_id. It does not return any value.

    Parameters:
    -----------
    character_server_id : int
        The ID of the CharacterServer record to be deleted.

    Returns:
    --------
    None
    """
    await CharacterServer.filter(id=character_server_id).delete()
