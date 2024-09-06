from discord import Embed, Colour
from settings import GEAR_PROGRESSION,WOWHEAD_SEASON_GEAR_GUIDE

async def generate_gear_embed():
    embed = Embed(
        title="TWW Gearing Guide",
        description=f"[Detail Information]({WOWHEAD_SEASON_GEAR_GUIDE})",
        colour=Colour.gold()
    )
    
    embed.set_image(url=GEAR_PROGRESSION)
    return embed
