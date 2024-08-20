import discord

from scripts.token.scrape_token import fetch_info_token
from embeds.wow_token_embed import generate_wow_token_embed
from utils.in_correct_channel import in_correct_channel
from utils.wow_regions_options import region_options


@discord.app_commands.command(
    name="token",
    description="Check WoW Token price for selected region",
)
@discord.app_commands.describe(region=f"Pick your region: EU, US, KR, TW")
@in_correct_channel()
async def token(interaction: discord.Interaction, region: region_options):
    """
    Fetches and displays the WoW Token price for the selected region.

    Args:
        interaction (discord.Interaction): The interaction object representing the command invocation.
        region (token_options): The region to fetch the token price for (EU, US, KR, or TW).

    Returns:
        None
    """
    fetch_data = fetch_info_token(region)
    token_embed = await generate_wow_token_embed(*fetch_data)

    await interaction.response.send_message(embed=token_embed)


def setup(client):
    client.tree.add_command(token)
