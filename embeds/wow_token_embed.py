from discord import Embed, Colour
from settings import TOKEN_PICTURE_URL
from utils.emojis_discord.common_emojis import common_emojis
from utils.emojis_discord.region_emojis import region_emojis
import datetime


async def generate_wow_token_embed(
    price: str,
    change: str,
    one_day_low: str,
    seven_day_low: str,
    thirty_day_low: str,
    one_day_high: str,
    seven_day_high: str,
    thirty_day_high: str,
    flag_region: str,
):
    """
    Generate an embed for WoW token information.

    Args:
        price (str): Current token price.
        change (str): Price change.
        one_day_low (str): Lowest price in the last day.
        seven_day_low (str): Lowest price in the last 7 days.
        thirty_day_low (str): Lowest price in the last 30 days.
        one_day_high (str): Highest price in the last day.
        seven_day_high (str): Highest price in the last 7 days.
        thirty_day_high (str): Highest price in the last 30 days.
        flag_region (str): Flag emoji representing the region.

    Returns:
        discord.Embed: An embed containing WoW token price information.
    """
    moneybag_icon = common_emojis.get("moneybag")
    embed = Embed(
        title=f"**Current Token Price {flag_region} {price} {moneybag_icon}**",
        description=f"**Change {change} {moneybag_icon}**",
        colour=Colour.blue(),
    )
    embed.set_thumbnail(url=TOKEN_PICTURE_URL)
    embed_field_data = [
        {
            "name": "**3 DAY**",
            "value": f"***Low : {one_day_low} {moneybag_icon}\n"
            f"High : {one_day_high} {moneybag_icon}***",
            "inline": True,
        },
        {
            "name": "**7 DAY**",
            "value": f"***Low : {seven_day_low} {moneybag_icon}\n"
            f"High : {seven_day_high} {moneybag_icon}***",
            "inline": True,
        },
        {
            "name": "**30 DAY**",
            "value": f"***Low : {thirty_day_low} {moneybag_icon}\n"
            f"High : {thirty_day_high} {moneybag_icon}***",
            "inline": True,
        },
    ]
    for field in embed_field_data:
        embed.add_field(**field)
    return embed


def generate_wow_token_embed_from_battle_net(price: int, region: str) -> Embed:
    moneybag_icon = common_emojis.get("moneybag")
    flag_icon = region_emojis.get(region.lower())
    embed = Embed(
        title=f"**Region {flag_icon} **",
        colour=Colour.blue(),
    )
    embed_field_data = [
        {
            "name": "Token Price",
            "value": f"**{price:,.0f}** {moneybag_icon}",
            "inline": True,
        },
    ]

    embed.set_thumbnail(url=TOKEN_PICTURE_URL)
    [embed.add_field(**field) for field in embed_field_data]

    return embed
