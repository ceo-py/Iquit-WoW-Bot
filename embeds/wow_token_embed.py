from discord import Embed, Colour
from settings import TOKEN_PICTURE_URL


def generate_wow_token_embed_from_battle_net(
    price: int, moneybag_icon: str, flag_icon: str
) -> Embed:
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
