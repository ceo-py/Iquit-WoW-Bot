from discord import Embed, Colour
from utils.emojis_discord.character_emojis import character_emojis
from settings import (
    FOOTER_EMBED_PICTURE_URL,
    WOW_LOG_BASE_URL,
    RAIDBOTS_BASE_URL,
    WOW_BASE_URL,
)


async def generate_check_embed(
    name: str,
    character_class: str,
    region: str,
    realm: str,
    active_spec_name: str,
    profile_url: str,
    thumbnail_url: str,
    gear_ilvl: str,
    dungeon_name: str,
    dungeon_key_lvl: str,
    dungeon_upgrade: str,
    dungeon_score: str,
    tank_score: str,
    dps_score: str,
    healer_score: str,
    raid_name: str,
    raid_progress_normal: str,
    raid_progress_heroic: str,
    raid_progress_mythic: str,
    total_raid_bosses: str,
):
    embed = Embed(
        title=f"{character_emojis.get(character_class.lower())} {name}, {active_spec_name}, {gear_ilvl} ILVL",
        description=f"**Mythic+ Score**",
        colour=Colour.gold(),
    )
    embed.set_thumbnail(url=thumbnail_url)
    embed.set_image(url=FOOTER_EMBED_PICTURE_URL)
    embed_field_data = [
        {
            "name": ":shield:",
            "value": f"{tank_score}",
            "inline": True,
        },
        {
            "name": ":crossed_swords:",
            "value": f"{dps_score}",
            "inline": True,
        },
        {
            "name": ":heart:",
            "value": f"{healer_score}",
            "inline": True,
        },
        {
            "name": f"**{raid_name}**",
            "value": f"{raid_progress_normal} / {total_raid_bosses}",
            "inline": True,
        },
        {
            "name": f"**Heroic**",
            "value": f"{raid_progress_heroic} / {total_raid_bosses}",
            "inline": True,
        },
        {
            "name": f"**Mythic**",
            "value": f"{raid_progress_mythic} / {total_raid_bosses}",
            "inline": True,
        },
        {
            "name": f"**Last Played Dungeon**",
            "value": f"{dungeon_name}",
            "inline": False,
        },
        {
            "name": f"**Key Level**",
            "value": f"{dungeon_key_lvl}",
            "inline": True,
        },
        {
            "name": f"**Key Upgrade**",
            "value": f"{dungeon_upgrade}",
            "inline": True,
        },
        {
            "name": f"**Points**",
            "value": f"{dungeon_score}",
            "inline": True,
        },
        {
            "name": f"**Useful Links**",
            "value": f"- [{name} Raider IO Profile]({profile_url})\n"
            f"- [{name} Armory Profile]({WOW_BASE_URL}{region}/character/{region}/{realm}/{name})\n"
            f"- [Simulate {name} on RaidBots]({RAIDBOTS_BASE_URL}{region}&realm={realm}&name={name})\n"
            f"- [{name} Warcraft Logs Profile]({WOW_LOG_BASE_URL}{region}/{realm}/{name})",
            "inline": True,
        },
    ]
    for field in embed_field_data:
        embed.add_field(**field)
    return embed
