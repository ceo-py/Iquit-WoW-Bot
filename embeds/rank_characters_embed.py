import discord
from discord import Embed
from settings import (
    WOW_CURRENT_EXPANSION,
    WOW_CURRENT_SEASON,
    RANK_THUMBNAIL,
    RAIDER_IO_BASE_URL_FOR_RANK,
    ARCHON_URL,
)
from utils.api.request_cut_off_information import get_wow_cut_offs
from utils.api.request_affixes_information import get_wow_affixes
from utils.character.character_ranking import format_ranks_for_embed


def get_discord_region_base_on_characters(characters: list) -> str:
    regions = {}
    for character in characters:
        regions[character.region] = regions.get(character.region, 0) + 1
    return max(regions, key=regions.get)


async def generate_rank_characters_embed(
    characters: list, interaction: discord.Interaction
) -> Embed:

    region = get_discord_region_base_on_characters(characters)

    embed = discord.Embed(
        title=f"Mythic+ Rankings {WOW_CURRENT_EXPANSION} Season {WOW_CURRENT_SEASON} - Leaderboard",
        colour=discord.Colour.blue(),
    )
    embed.set_thumbnail(url=RANK_THUMBNAIL)

    characters_with_total_rating = format_ranks_for_embed(characters, "total", 9)
    characters_with_dps_rating = format_ranks_for_embed(characters, "dps", 3)
    characters_with_heal_rating = format_ranks_for_embed(characters, "heal", 3)
    characters_with_tank_rating = format_ranks_for_embed(characters, "tank", 3)

    cut_offs = await get_wow_cut_offs(region, WOW_CURRENT_EXPANSION, WOW_CURRENT_SEASON)
    cut_offs_message = None

    if cut_offs.get("cutoffs") is None:
        cut_offs_message = "No information available"

    embed_fields = [
        {
            "name": f"**{interaction.client.region_emojis.get(region.lower())} Rating Cutoffs**",
            "value": f"```" f"{cut_offs_message}```",
            "inline": False,
        },
        {
            "name": "**:regional_indicator_t::regional_indicator_o::regional_indicator_p: :nine:**",
            "value": "\n".join(str(c) for c in characters_with_total_rating[:3]),
            "inline": True,
        },
        {
            "name": ":arrow_down_small:",
            "value": "\n".join(str(c) for c in characters_with_total_rating[3:6]),
            "inline": True,
        },
        {
            "name": ":arrow_down_small:",
            "value": "\n".join(str(c) for c in characters_with_total_rating[6:]),
            "inline": True,
        },
        {
            "name": ":regional_indicator_t::regional_indicator_o::regional_indicator_p: :three:",
            "value": "**Ranking by roles:**",
            "inline": False,
        },
        {
            "name": f"{interaction.client.character_role_emojis.get('dps')}",
            "value": "\n".join(str(c) for c in characters_with_dps_rating),
            "inline": True,
        },
        {
            "name": f"{interaction.client.character_role_emojis.get('healer')}",
            "value": "\n".join(str(c) for c in characters_with_heal_rating),
            "inline": True,
        },
        {
            "name": f"{interaction.client.character_role_emojis.get('tank')}",
            "value": "\n".join(str(c) for c in characters_with_tank_rating),
            "inline": True,
        },
        {
            "name": "This Week Affixes",
            "value": f"[{await get_wow_affixes(region)}]({ARCHON_URL})",
            "inline": False,
        },
        {
            "name": f"**World Top Ranks Season {WOW_CURRENT_SEASON} {WOW_CURRENT_EXPANSION}**",
            "value": f"[Mythic+ Rankings for All Classes & Roles]"
            f"({RAIDER_IO_BASE_URL_FOR_RANK}-{WOW_CURRENT_EXPANSION.lower()}-{WOW_CURRENT_SEASON}/world/all/all)\n "
            f"[Mythic+ Rankings for All Tanks]"
            f"({RAIDER_IO_BASE_URL_FOR_RANK}-{WOW_CURRENT_EXPANSION.lower()}-{WOW_CURRENT_SEASON}/world/all/tank)\n "
            f"[Mythic+ Rankings for All Healers]"
            f"({RAIDER_IO_BASE_URL_FOR_RANK}-{WOW_CURRENT_EXPANSION.lower()}-{WOW_CURRENT_SEASON}/world/all/healer)\n "
            f"[Mythic+ Rankings for All DPS]"
            f"({RAIDER_IO_BASE_URL_FOR_RANK}-{WOW_CURRENT_EXPANSION.lower()}-{WOW_CURRENT_SEASON}/world/all/dps)",
            "inline": False,
        },
    ]

    [embed.add_field(**fields) for fields in embed_fields]
    return embed
