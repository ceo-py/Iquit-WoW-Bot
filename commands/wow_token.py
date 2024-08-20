import discord
from typing import Literal

token_options = Literal["EU", "US", "KR", "TW"]


@discord.app_commands.command(
    name="token",
    description="Check WoW Token price for selected region",
)
@discord.app_commands.describe(region=f"Pick your region: EU, US, KR, TW")
async def token(
        interaction: discord.Interaction, region: token_options
):
    output = f"You`ve selected region {region}"

    await interaction.response.send_message(output)


def setup(client):
    client.tree.add_command(token)

