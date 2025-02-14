import discord
from utils.permissions.in_correct_channel import in_correct_channel
from utils.permissions.is_bot_owner import is_bot_owner


@discord.app_commands.command(
    name="reset_season",
    description="Reset all character data for the new season",
)
@in_correct_channel()
@is_bot_owner()
async def reset_season(interaction: discord.Interaction):
    """
    Resets all character data for the new season in the specified region.

    Args:
        interaction (discord.Interaction): The interaction object representing the command invocation.
        region (region_options): The region where to reset the data (EU, US, KR, or TW).

    Returns:
        None
    """
    await interaction.response.defer()
    await interaction.followup.send("pass")


def setup(client):
    client.tree.add_command(reset_season)
