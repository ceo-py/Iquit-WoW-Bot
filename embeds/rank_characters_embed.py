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


def generate_cut_off_message(
    cut_offs: dict, interaction: discord.Interaction, region: str
) -> list[dict]:
    ranks = [0.1, 1, 10]
    sides = ["all", "horde", "alliance"]
    cut_offs_top_ranks_keys = ["p999", "p990", "p900"]
    cut_offs_number_ranks = {r: {} for r in ranks}
    cut_offs = cut_offs.get("cutoffs")

    if cut_offs is None:
        return [
            {
                "name": f"**{interaction.client.region_emojis.get(region.lower())} Rating Cutoffs**",
                "value": f"```n/a```",
                "inline": False,
            },
        ]
    horde_icon = interaction.client.common_emojis.get("horde")
    alliance_icon = interaction.client.common_emojis.get("alliance")
    region_icon = interaction.client.region_emojis.get(region.lower())

    for index_, cut_off in enumerate(cut_offs_top_ranks_keys):
        cut_off_top = cut_offs.get(cut_off)
        if not cut_off_top:
            continue
        cut_offs_number_ranks[ranks[index_]] = {
            side: cut_off_top.get(side, {}).get("quantileMinValue", 0) for side in sides
        }

    # TODO : fix issue if no cut offs are found
    try:
        output = [
            {
                "name": f"**{region_icon}{horde_icon}{alliance_icon} Cutoffs**",
                "value": "\n".join(
                    f'Top {str(cut_off_key)}% - {cut_offs_number_ranks.get(cut_off_key, {}).get("all")}'
                    for cut_off_key in cut_offs_number_ranks
                ),
                "inline": True,
            },
            {
                "name": f"{horde_icon}",
                "value": "\n".join(
                    f'{str(r.get("horde"))}' for r in cut_offs_number_ranks.values()
                ),
                "inline": True,
            },
            {
                "name": f"{alliance_icon}",
                "value": "\n".join(
                    f'{str(r.get("alliance"))}' for r in cut_offs_number_ranks.values()
                ),
                "inline": True,
            },
        ]
    except Exception as e:
        print(f"Exception in generate_cut_off_message\n{e}")
        return []
    return output


async def generate_rank_characters_embed(
    characters: list, interaction: discord.Interaction
) -> Embed:

    RANK_URL_RAIDER_IO = f"{RAIDER_IO_BASE_URL_FOR_RANK}-{WOW_CURRENT_EXPANSION.lower()}-{WOW_CURRENT_SEASON}/world/all"
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

    cut_offs = await get_wow_cut_offs(
        region, WOW_CURRENT_EXPANSION.lower(), WOW_CURRENT_SEASON
    )
    cut_offs_message = generate_cut_off_message(cut_offs, interaction, region)

    # print(cut_offs_message)

    embed_fields = [
        *cut_offs_message,
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
            f"({RANK_URL_RAIDER_IO}/all)\n "
            f"[Mythic+ Rankings for All Tanks]"
            f"({RANK_URL_RAIDER_IO}/tank)\n "
            f"[Mythic+ Rankings for All Healers]"
            f"({RANK_URL_RAIDER_IO}/healer)\n "
            f"[Mythic+ Rankings for All DPS]"
            f"({RANK_URL_RAIDER_IO}/dps)",
            "inline": False,
        },
    ]

    [embed.add_field(**fields) for fields in embed_fields]
    return embed
