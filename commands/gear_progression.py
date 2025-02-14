import discord
from utils.permissions.in_correct_channel import in_correct_channel
from embeds.gear_command_embed import generate_gear_embed


@discord.app_commands.command(
    name="gear",
    description="TWW Gearing Guide Infographic.",
)
@in_correct_channel()
async def gear(interaction: discord.Interaction):
    """
    Sends the TWW Gearing Guide Infographic to the Discord channel.

    Args:
        interaction (discord.Interaction): The interaction object representing the command invocation.

    Returns:
        None
    """
    await interaction.response.defer()
    gear_embed = await generate_gear_embed()

    await interaction.followup.send(embed=gear_embed)


def setup(client):
    client.tree.add_command(gear)
