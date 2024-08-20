import discord
from typing import Literal
from scripts.token.scrape_token import fetch_info_token
from embeds.wow_token_embed import generate_wow_token_embed

token_options = Literal["EU", "US", "KR", "TW"]


@discord.app_commands.command(
    name="token",
    description="Check WoW Token price for selected region",
)
@discord.app_commands.describe(region=f"Pick your region: EU, US, KR, TW")
async def token(
        interaction: discord.Interaction, region: token_options
):
    fetch_data = fetch_info_token(region)
    token_embed = await generate_wow_token_embed(*fetch_data)

    await interaction.response.send_message(embed=token_embed)


def setup(client):
    client.tree.add_command(token)

