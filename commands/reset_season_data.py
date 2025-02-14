import discord

from embeds.wow_token_embed import generate_wow_token_embed_from_battle_net
from utils.permissions.in_correct_channel import in_correct_channel
from utils.wow_regions_options import region_options
from utils.token.get_token_price import get_token_price


@discord.app_commands.command(
    name="reset_season",
    description="Reset all character data for the new season",
)
@discord.app_commands.describe(region="Reset all character data for the new season")
@in_correct_channel()
async def reset_season(interaction: discord.Interaction, region: region_options):
    """
    Resets all character data for the new season in the specified region.

    Args:
        interaction (discord.Interaction): The interaction object representing the command invocation.
        region (region_options): The region where to reset the data (EU, US, KR, or TW).

    Returns:
        None
    """
    await interaction.response.defer()
    token_price = await get_token_price(region)
    token_embed = generate_wow_token_embed_from_battle_net(
        token_price,
        interaction.client.common_emojis.get("moneybag"),
        interaction.client.region_emojis.get(region.lower()),
    )

    await interaction.followup.send(embed=token_embed)


def setup(client):
    client.tree.add_command(reset_season)
