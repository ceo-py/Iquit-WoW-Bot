import discord
from utils.permissions.in_correct_channel import in_correct_channel
from modals.m_plus_best_runs_modal import MPlusBestRunsModal


@discord.app_commands.command(
    name="mplus",
    description="Display the top Mythic+ dungeon runs for a character across all dungeons.",
)
@in_correct_channel()
async def mplus(interaction: discord.Interaction):

    await interaction.response.send_modal(MPlusBestRunsModal())


def setup(client):
    client.tree.add_command(mplus)
