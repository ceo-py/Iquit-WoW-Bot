import discord
from discord import Embed
from settings import WOW_CURRENT_EXPANSION, WOW_CURRENT_SEASON, RANK_THUMBNAIL
from scripts.api.request_cut_off_information import get_wow_cut_offs



def get_discord_region_base_on_characters(characters: list) -> str:
    regions = {}
    for character in characters:
        regions[character.region] = regions.get(character.region, 0) + 1
    return max(regions, key=regions.get) 


async def generate_rank_characters_embed(characters: list, interaction: discord.Interaction) -> Embed:

    region = get_discord_region_base_on_characters(characters)
    print(region)

    embed = discord.Embed(
        title=f"Mythic+ Rankings {WOW_CURRENT_EXPANSION} Season {WOW_CURRENT_SEASON} - Leaderboard",
        colour=discord.Colour.blue(),
    )
    embed.set_thumbnail(
        url=RANK_THUMBNAIL
    )


    '''
    https://raider.io/api/v1/mythic-plus/season-cutoffs?season=season-tww-1&region=eu
    https://raider.io/api/v1/mythic-plus/season-cutoffs?season=season-df-{season}&region={region}
    '''
    cut_offs = await get_wow_cut_offs(region, WOW_CURRENT_EXPANSION, WOW_CURRENT_SEASON)
    cut_offs_message = None

    if cut_offs.get('error') == 'Not Found':
        cut_offs_message = "No information available"

        print(cut_offs)
    # data_db = await char_info.get_data_for_rank(cnl_id, None)
    # if data_db == 'Error':
    #     data_db = await char_info.get_data_for_rank(cnl_id, "Yes")
    #     return await backup_message(ctx, embed, data_db)

    # total = char_display.get_all_chars(char_display.sorting_db(data_db, "Total"))

    # region = await db_.get_region(cnl_id)

    # if region:
    #     top_cut_offs = "\n".join(
    #         f"{name} - {rating:.1f}" for rating, name in get_wow_cutoff(region, SEASON)
    #     )
    #     embed.add_field(
    #         name="**Mythic+ Rating Cutoffs**",
    #         value=f"```" f"{top_cut_offs}```",
    #         inline=False,
    #     )

    embed_fields = [
        {
            'name': "**Mythic+ Rating Cutoffs**",
            'value': f"```" f"{cut_offs_message}```",
            'inline': True
        },
        {
            'name': "**:regional_indicator_t::regional_indicator_o::regional_indicator_p: :nine:**",
            'value': '',
            'inline': True
        },
        {
            'name': "**:regional_indicator_t::regional_indicator_o::regional_indicator_p: :nine:**",
            'value': '',
            'inline': True
        },
    ]
    '''
    embed.add_field(
        name="**:regional_indicator_t::regional_indicator_o::regional_indicator_p: :nine:**",
        value=f"{total[1]}\n{total[2]}\n" f"{total[3]}",
        inline=True,
    )

    embed.add_field(
        name=":arrow_down_small:",
        value=f"{total[4]}\n{total[5]}\n{total[6]}",
        inline=True,
    )

    embed.add_field(
        name=":arrow_down_small:",
        value=f"{total[7]}\n{total[8]}\n{total[9]}",
        inline=True,
    )

    embed.add_field(
        name=":regional_indicator_t::regional_indicator_o::regional_indicator_p: :three:",
        value="**Ranking by roles:**",
        inline=False,
    )

    dps = char_display.get_other_ranks(
        char_display.sorting_db(data_db, "DPS"), "DPS"
    )
    embed.add_field(
        name=f"{emojis('dps')}",
        value=f":first_place:{dps[1]}\n:second_place:{dps[2]}\n:third_place:{dps[3]}",
        inline=True,
    )

    heal = char_display.get_other_ranks(
        char_display.sorting_db(data_db, "Heal"), "Heal"
    )
    embed.add_field(
        name=f"{emojis('healer')}",
        value=f":first_place:{heal[1]}\n:second_place:{heal[2]}\n:third_place:{heal[3]}",
        inline=True,
    )

    tank = char_display.get_other_ranks(
        char_display.sorting_db(data_db, "Tank"), "Tank"
    )
    embed.add_field(
        name=f"{emojis('tank')}",
        value=f":first_place:{tank[1]}\n:second_place:{tank[2]}\n:third_place:{tank[3]}",
        inline=True,
    )

    embed.add_field(
        name="This Week Affixes",
        value=f"[{get_affixes()}](https://mplus.subcreation.net/index.html)",
        inline=False,
    )

    embed.add_field(
        name=f"**World Top Ranks Season {SEASON} {EXPANSION}**",
        value=f"[Mythic+ Rankings for All Classes & Roles]"
        f"(https://raider.io/mythic-plus-character-rankings/season-{EXPANSION.lower()}-{SEASON}/world/all/all)\n "
        f"[Mythic+ Rankings for All Tanks]"
        f"(https://raider.io/mythic-plus-character-rankings/season-{EXPANSION.lower()}-{SEASON}/world/all/tank)\n "
        f"[Mythic+ Rankings for All Healers]"
        f"(https://raider.io/mythic-plus-character-rankings/season-{EXPANSION.lower()}-{SEASON}/world/all/healer)\n "
        f"[Mythic+ Rankings for All DPS]"
        f"(https://raider.io/mythic-plus-character-rankings/season-{EXPANSION.lower()}-{SEASON}/world/all/dps)",
        inline=False,
    )
    '''
    for fields in embed_fields:
        embed.add_field(**fields)
    return embed
