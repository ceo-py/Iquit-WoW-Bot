import discord
from utils.in_correct_channel import in_correct_channel
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
    gear_embed = await generate_gear_embed()

    await interaction.response.send_message(embed=gear_embed)


def setup(client):
    client.tree.add_command(gear)
