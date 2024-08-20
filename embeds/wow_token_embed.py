from discord import Embed, Colour
from settings import TOKEN_PICTURE_URL


async def generate_wow_token_embed(price,
                                   change,
                                   one_day_low,
                                   seven_day_low,
                                   thirty_day_low,
                                   one_day_high,
                                   seven_day_high,
                                   thirty_day_high,
                                   flag_region):
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
    moneybag_icon = ":moneybag:"
    embed = Embed(
        title=f"**Current Token Price {flag_region} {price} {moneybag_icon}**",
        description=f"**Change {change} {moneybag_icon}**",
        colour=Colour.blue(),
    )
    embed.set_thumbnail(
        url=TOKEN_PICTURE_URL
    )
    embed_field_data = [
        {"name": "**3 DAY**",
         "value": f"***Low : {one_day_low} {moneybag_icon}\n"
         f"High : {one_day_high} {moneybag_icon}***",
         "inline": True},
        {"name": "**7 DAY**",
         "value": f"***Low : {seven_day_low} {moneybag_icon}\n"
                  f"High : {seven_day_high} {moneybag_icon}***",
                  "inline": True},
        {"name": "**30 DAY**",
         "value": f"***Low : {thirty_day_low} {moneybag_icon}\n"
         f"High : {thirty_day_high} {moneybag_icon}***",
         "inline": True},
    ]
    for field in embed_field_data:
        embed.add_field(**field)
    return embed