import discord
from utils.in_correct_channel import in_correct_channel
from modals.add_character_to_server_modal import AddCharacterModal


@discord.app_commands.command(
    name="gear",
    description="TWW Gearing Guide Infographic.",
)
@in_correct_channel()
async def gear(interaction: discord.Interaction):

    """
    Fetches and displays the WoW Token price for the selected region.

    Args:
        interaction (discord.Interaction): The interaction object representing the command invocation.
        region (token_options): The region to fetch the token price for (EU, US, KR, or TW).

    Returns:
        None
    """

    await interaction.response.send_message(embed=token_embed)


def setup(client):
    client.tree.add_command(gear)
