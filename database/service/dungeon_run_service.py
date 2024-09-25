from database.models.dungeon_run import DungeonRun


async def create_dungeon_run(
    character_id: int,
    dungeon_id: int,
    mythic_level: int,
    num_keystone_upgrades: int,
    clear_time_ms: int,
    par_time_ms: int,
    score: int,
    affix_types: list[str],
) -> DungeonRun:
    """
    Create a new DungeonRun instance and save it to the database.

    This function creates a new DungeonRun record in the database using the
    provided parameters.

    Parameters:
    -----------
    character_id : int
        The character ID who completed the dungeon run.
    dungeon_id : int
        The dungeon ID that was run.
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
    affix_types : list[str]
        The type of affixes active during the run.

    Returns:
    --------
    DungeonRun
        The newly created DungeonRun instance.

    """
    dungeon = await DungeonRun.create(
        character_id=character_id,
        dungeon_id=dungeon_id,
        mythic_level=mythic_level,
        num_keystone_upgrades=num_keystone_upgrades,
        clear_time_ms=clear_time_ms,
        par_time_ms=par_time_ms,
        score=score,
        affix_types=affix_types,
    )
    return dungeon
