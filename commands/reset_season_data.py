import discord
from utils.permissions.in_correct_channel import in_correct_channel
from utils.permissions.is_bot_owner import is_bot_owner
from database.service.character_service import reset_all_character_ratings
from database.service.dungeon_run_service import reset_all_character_dungeon_runs
from database.service.character_server_service import reset_all_character_server_rankings


@discord.app_commands.command(
    name="reset_season",
    description="Resets all character data for new season",
)
@in_correct_channel()
@is_bot_owner()
async def reset_season(interaction: discord.Interaction):
    """
    Resets all character data for new season.
    Args:
        interaction (discord.Interaction): The interaction object representing the command invocation.

    Returns:
        None
    """
    reset_count = await reset_all_character_ratings()
    reset_dungeons_count = await reset_all_character_dungeon_runs()
    reset_rankings_count = await reset_all_character_server_rankings()

    await interaction.response.defer()
    await interaction.followup.send(f"Reset {reset_count} characters, {reset_rankings_count} server rankings, and {reset_dungeons_count} dungeon runs!")

def setup(client):
    client.tree.add_command(reset_season)
