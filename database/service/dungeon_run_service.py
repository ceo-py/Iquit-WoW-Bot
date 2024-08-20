from database.models.dungeon_run import DungeonRun


async def create_dungeon_run(
    character: str,
    dungeon: str,
    mythic_level: int,
    num_keystone_upgrades: int,
    clear_time_ms: int,
    par_time_ms: int,
    score: int,
    affix_type: str,
) -> DungeonRun:
    """
    Create a new DungeonRun instance and save it to the database.

    This function creates a new DungeonRun record in the database using the
    provided parameters.

    Parameters:
    -----------
    character : str
        The name of the character who completed the dungeon run.
    dungeon : str
        The name of the dungeon that was run.
    mythic_level : int
        The mythic+ level of the dungeon run.
    num_keystone_upgrades : int
        The number of keystone upgrades achieved in the run.
    clear_time_ms : int
        The time taken to clear the dungeon, in milliseconds.
    par_time_ms : int
        The par time for the dungeon, in milliseconds.
    score : int
        The score achieved for the dungeon run.
    affix_type : str
        The type of affixes active during the run.

    Returns:
    --------
    DungeonRun
        The newly created DungeonRun instance.

    """
    dungeon = await DungeonRun.create(
        character=character,
        dungeon=dungeon,
        mythic_level=mythic_level,
        num_keystone_upgrades=num_keystone_upgrades,
        clear_time_ms=clear_time_ms,
        par_time_ms=par_time_ms,
        score=score,
        affix_type=affix_type,
    )
    return dungeon
