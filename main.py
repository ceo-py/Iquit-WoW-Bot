import discord
import os
from dotenv import load_dotenv
from discord_buttons_plugin import *
from other_commands import weather_check, ask_question, get_info_token, get_affixes
from data_base_info import DataBaseInfo
from character_info import CharacterInfo
from sorting_ranks import RankCharacterDisplay
# from api_calls_db import APICALLDB
from discord.ext import commands

# from discord import embeds

# api_ = APICALLDB()
char_db = DataBaseInfo()
char_info = CharacterInfo()
char_display = RankCharacterDisplay()
client = commands.Bot(command_prefix="!", help_command=None)
load_dotenv()
TOKEN = os.getenv("TOKEN")
# DISCORD_CHANNEL_NAME = "iquit-bot"
DISCORD_CHANNEL_NAME = "test-robot"
buttons = ButtonsClient(client)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Waiting for Sunset'))
    print("Ready")


@client.command()
async def rank(ctx):
    cnl_id = await msg_check(ctx)
    if cnl_id:
        embed = discord.Embed(
            title="Mythic+ Rankings SL Season 3 - Leaderboard",
            # description="This is current score from added characters, if you want to compere yours type `!cadd region realm name yournickname class`, "
            #             "example `!cadd eu draenor ceomerlin ceo warlock`. That way you will add your character into the list, then you can ask for `!check ceo warlock` dont need to type"
            #             " everything like `!check eu draenor ceomerlin`",
            colour=discord.Colour.blue()
        )
        embed.set_thumbnail(url="https://graphly.io/wp-content/uploads/leaderboards-podium-star.jpg")

        data_db_data = await char_info.get_data_for_rank(cnl_id)
        data_db = rank_data(data_db_data, "Total")
        embed.add_field(name="**:regional_indicator_t::regional_indicator_o::regional_indicator_p: :nine:**",
                        value=f"{data_db[1]}\n{data_db[2]}\n"
                              f"{data_db[3]}", inline=True)
        embed.add_field(name=":arrow_down_small:",
                        value=f"{data_db[4]}\n{data_db[5]}\n{data_db[6]}",
                        inline=True)
        embed.add_field(name=":arrow_down_small:",
                        value=f"{data_db[7]}\n{data_db[8]}\n{data_db[9]}",
                        inline=True)
        embed.add_field(name=":regional_indicator_t::regional_indicator_o::regional_indicator_p: :three:",
                        value="**Ranking by roles:**", inline=False)
        data_db = rank_data(data_db_data, "DPS")
        embed.add_field(name=":crossed_swords:",
                        value=f":first_place:{data_db[1]}\n:second_place:{data_db[2]}\n:third_place:{data_db[3]}",
                        inline=True)
        data_db = rank_data(data_db_data, "Heal")
        embed.add_field(name=":heart:",
                        value=f":first_place:{data_db[1]}\n:second_place:{data_db[2]}\n:third_place:{data_db[3]}",
                        inline=True)
        data_db = rank_data(data_db_data, "Tank")
        embed.add_field(name=":shield:",
                        value=f":first_place:{data_db[1]}\n:second_place:{data_db[2]}\n:third_place:{data_db[3]}",
                        inline=True)
        embed.add_field(name="This Week Affixes",
                        value=f"[**{get_affixes()}**](https://mplus.subcreation.net/index.html)", inline=False)
        embed.add_field(name="World Top Ranks",
                        value="[**Mythic+ Rankings for All Classes & Roles (SL Season 3)**]("
                              "https://raider.io/mythic-plus-character-rankings/season-sl-3/world/all/all)\n "
                              "[**Mythic+ Rankings for All Tanks (SL Season 3)**]("
                              "https://raider.io/mythic-plus-character-rankings/season-sl-3/world/all/tank)\n "
                              "[**Mythic+ Rankings for All Healers (SL Season 3)**]("
                              "https://raider.io/mythic-plus-character-rankings/season-sl-3/world/all/healer)\n "
                              "[**Mythic+ Rankings for All DPS (SL Season 3)**]("
                              "https://raider.io/mythic-plus-character-rankings/season-sl-3/world/all/dps)",
                        inline=False)
        await ctx.send(embed=embed)
        await discord_buttons_rank(cnl_id)


# @client.command()
# async def check(ctx, arg1, arg2, *args):
#     cnl_id = await msg_check(ctx)
#     if cnl_id:
#         #to do check nick in db
#         embed = discord.Embed(
#             title=str(score) + " - Best Mythic+ Score",
#             description=f"[Character Link]({purl}) :link: "f"[Armory Profile](https://worldofwarcraft.com/en-{rio_character.region}/character/{rio_character.region}/{rio_character.realm}/{rio_character.name})\n"
#                         f"[Simulate on RaidBots](https://www.raidbots.com/simbot/quick?region={rio_character.region}&realm={rio_character.realm}&name={rio_character.name}) :link: "
#                         f"[Warcraft Logs Profile](https://www.warcraftlogs.com/character/{rio_character.region}/{rio_character.realm}/{rio_character.name})",
#             colour=discord.Colour.blue()
#         )
#         embed.set_thumbnail(url=tmbn)
#         embed.set_author(name='{}, {}, {}, {}, {} ILVL'.format(name, spec, c, cname, str(renown_level), str(ilvl)),
#                          icon_url=class_icon)
#         embed.add_field(name=":shield:", value=tank, inline=True)
#         embed.add_field(name=":crossed_swords:", value=dps, inline=True)
#         embed.add_field(name=":green_heart:", value=healer, inline=True)
#         embed.add_field(name="Sanctum of Domination Normal", value="{}" "/10".format(str(nprog)), inline=True)
#         embed.add_field(name="Heroic", value="{}" "/10".format(str(hprog)), inline=True)
#         embed.add_field(name="Mythic", value="{}" "/10".format(str(mprog)), inline=True)
#         embed.add_field(name="Sepulcher of the First Ones Normal", value="{}" "/11".format(str(nsprog)),
#                         inline=True)
#         embed.add_field(name="Heroic", value="{}" "/11".format(str(hsprog)), inline=True)
#         embed.add_field(name="Mythic", value="{}" "/11".format(str(msprog)), inline=True)
#         # embed.add_field(name="Character Link", value=purl)
#         embed.add_field(name="Last Finished Dungeon", value="{}" "".format(str(lfinish)), inline=False)
#         embed.add_field(name="Key Level", value="{}" "".format(str(keylevel)), inline=True)
#         embed.add_field(name="Key Upgrade", value="{}" "".format(str(keyup)), inline=True)
#         embed.add_field(name="Points", value="{}" "".format(str(rscore)), inline=True)
#         embed.add_field(name="Current Affixes",
#                         value="[**{}**](https://mplus.subcreation.net/index.html)".format(affix), inline=False)
#         await msg_send.send(embed=embed)


@client.command()
async def cadd(ctx, *c_data_input):
    cnl_id = await msg_check(ctx)
    if cnl_id:
        if len(c_data_input) != 5:
            await ctx.send(
                "Not valid information, check what you type! The Right format is:```!cadd eu draenor ceomerlin ceo "
                "warlock```")
            return
        await ctx.send(char_info.check_if_correct_cadd(c_data_input, cnl_id))


@client.command()
async def help(ctx):
    cnl_id = await msg_check(ctx)
    if cnl_id:
        embed = discord.Embed(
            title="Help Center For Iquit Commands",
            colour=discord.Colour.blue()
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/880059629252534292/880060565190500423/iq.png")
        embed.add_field(name="**!check region realm character name**",
                        value="[Example](https://cdn.discordapp.com/attachments/880059629252534292/880077926505250846"
                              "/check.png) `!check eu draenor ceomerlin` with this command "
                              "you are going to see that character current progress in raids, raider IO, last timed "
                              "key and more.\n :arrow_down: ",
                        inline=False)
        embed.add_field(name="**!cadd region realm character name your nick name character class**",
                        value="Example `!cadd eu draenor ceomerlin ceo warlock` with this command you are going to add"
                              "that character into the list. Ones that is done you can use quick [`!check ceo "
                              "warlock`](https://cdn.discordapp.com/attachments/880059629252534292/880077999880409088"
                              "/qcheck.png) "
                              "over typing `!cadd eu draenor ceomerlin` command and "
                              "that character will enter into the rank system where you can see where you rank "
                              "compere to your friends and other people that you add to the list. "
                              "The last two argumets in this example `!cadd eu draenor ceomerlin ceo warlock`, "
                              "`ceo warlock` are completely free to type what you like that you can "
                              "remember easy.\n :arrow_down: ", inline=False)
        embed.add_field(name="**!rank**",
                        value="[Example](https://cdn.discordapp.com/attachments/880059629252534292/880064020525223956"
                              "/rank.png) `!rank` with that command every character that "
                              "you add already to the list with `!cadd` command will be compere and ranked by raider "
                              "IO with total section dont matter the role and separate "
                              " ranks for DPS, Healers and Tanks.\n :arrow_down: ", inline=False)
        embed.add_field(name="**!token region**",
                        value="[Example](https://cdn.discordapp.com/attachments/880059629252534292/880153278111961108"
                              "/token.png) `!token eu`, `!token us`, `!token china`, `!token korea`, `!token taiwan` "
                              " with that command you can check token prices in every region.\n :arrow_down: ",
                        inline=False)
        embed.add_field(name="**!weather city**",
                        value="[Example](https://cdn.discordapp.com/attachments/880059629252534292/880154617730703390"
                              "/weather.png) `!weather sofia` "
                              "with that command you can check the weather in your city or where you want.\n "
                              ":arrow_down: ",
                        inline=False)
        embed.add_field(name="**!ask question**",
                        value="[Example](https://cdn.discordapp.com/attachments/880059629252534292/880155463759581194"
                              "/ask.png) `!ask 2+2`, `!ask capital bulgaria`, `!ask next nba game` "
                              "with that command you can ask simple questions like you ask your google or amazon "
                              "assistance.",
                        inline=False)
        await ctx.send(embed=embed)


@client.command()
async def weather(ctx, arg1=None):
    cnl_id = await msg_check(ctx)
    if cnl_id:
        if arg1 is None:
            await ctx.send(
                f"Make sure you type town name.\nExample **!weather Sofia**")
            return
        t, t_min, t_max, feels_like = weather_check(arg1)
        embed = discord.Embed(
            title=f"Temperature in {arg1.capitalize()} is {t} °C",
            colour=discord.Colour.blue()
        )
        embed.set_thumbnail(url="https://flyclipart.com/downloadpage/images/sun-png-transparent-background-transparent-sun-transparent-375282.png/375282")
        embed.add_field(name="Feels :sunny:", value=f"{feels_like} °C", inline=False)
        embed.add_field(name="Min Temperature : ", value=f"{t_min} °C", inline=True)
        embed.add_field(name="Max Temperature : ", value=f"{t_max} °C", inline=True)
        await ctx.send(embed=embed)


@client.command()
async def ask(ctx, *args):
    cnl_id = await msg_check(ctx)
    if cnl_id:
        if not args:
            await ctx.send(
                f"Make sure you type your question.\nExample **!ask what is capital of USA**")
            return
        status_code, answer_to_show = ask_question(args)
        if status_code == 501:
            await ctx.send("Meh I`m Stupid don`t know the answer!")
        else:
            embed = discord.Embed(
                title=answer_to_show,
                colour=discord.Colour.blue()
            )
            await ctx.send(embed=embed)


@client.command()
async def token(ctx, region=None):
    cnl_id = await msg_check(ctx)
    if cnl_id:
        if region is None:
            await ctx.send(
                f"Make sure you type right region.\nRegions are: us, eu, china, korea, taiwan\nExample **!token eu**")
            return
        price, change, one_day_low, seven_day_low, thirty_day_low, one_day_high, \
        seven_day_high, thirty_day_high, flag_region = get_info_token(region)
        embed = discord.Embed(
            title=f"**Current Token Price {flag_region} {price} :moneybag:**",
            description=f"**Change {change} :moneybag:**",
            colour=discord.Colour.blue())
        embed.set_thumbnail(
            url="https://wowtokenprices.com/assets/wowtoken-compressed.png")
        embed.add_field(name="**1 DAY**", value=f"***Low : {one_day_low} :moneybag:\n"
                                                f"High : {one_day_high} :moneybag:***", inline=True)
        embed.add_field(name="**7 DAY**", value=f"***Low : {seven_day_low} :moneybag:\n"
                                                f"High : {seven_day_high} :moneybag:***", inline=True)
        embed.add_field(name="**30 DAY**", value=f"***Low : {thirty_day_low} :moneybag:\n"
                                                 f"High : {thirty_day_high} :moneybag:***", inline=True)
        await ctx.send(embed=embed)


async def msg_check(ctx):
    right_channel, msg_send, cnl_id = check_right_channel(ctx)
    if not right_channel:
        await ctx.author.send(
            f"Not Right Channel make sure you create text channel - **{DISCORD_CHANNEL_NAME}**, and send your commands "
            f"there!")
        return
    channel_data_ = char_db.connect_db(cnl_id, msg_check=True).find({"Channel Id": cnl_id})
    try:
        channel_data_[0]["Channel Id"]
    except IndexError:
        char_db.save_msg_id(msg_send, cnl_id)
    return cnl_id


def check_right_channel(ctx):
    if str(ctx.channel) == DISCORD_CHANNEL_NAME:
        return True, str(ctx.guild.id), str(ctx.channel.id)
    return False, 0, 0


def rank_data(data_base, type_of_rank):
    data_db = char_display.sorting_db(data_base, type_of_rank)
    if type_of_rank != "Total":
        return char_display.get_other_ranks(data_db, type_of_rank)
    return char_display.get_all_chars(data_db)


## buttons_commands


async def button_info_display(type_of_info, channel_id):
    data_db = await char_info.get_data_for_rank(channel_id)
    data_db = char_display.sorting_db(data_db, f"{type_of_info}")
    return char_display.button_rank_result(data_db, f"{type_of_info}")


@buttons.click
async def b_all_chars(ctx):
    cnl_id = await msg_check(ctx)
    if cnl_id:
        await ctx.reply(content=f"```TOP Total\n{await button_info_display('Total', cnl_id)}```", flags=MessageFlags().EPHEMERAL)


@buttons.click
async def b_all_dps(ctx):
    cnl_id = await msg_check(ctx)
    if cnl_id:
        await ctx.reply(content=f"```TOP DPS\n{await button_info_display('DPS', cnl_id)}```", flags=MessageFlags().EPHEMERAL)


@buttons.click
async def b_all_heal(ctx):
    cnl_id = await msg_check(ctx)
    if cnl_id:
        await ctx.reply(content=f"```TOP Healers\n{await button_info_display('Heal', cnl_id)}```", flags=MessageFlags().EPHEMERAL)


@buttons.click
async def b_all_tank(ctx):
    cnl_id = await msg_check(ctx)
    if cnl_id:
        await ctx.reply(content=f"```TOP Tanks\n{await button_info_display('Tank', cnl_id)}```", flags=MessageFlags().EPHEMERAL)


@client.command()
async def discord_buttons_rank(file_name):
    await buttons.send(
        content="**More detail information about TOP ranks below**",
        channel=file_name,
        components=[ActionRow([Button(style=ButtonType().Primary, label=" All Total Rank! ", custom_id="b_all_chars"),
                               Button(style=ButtonType().Success, label=" All Dps Ranks! ", custom_id="b_all_dps"),
                               Button(style=ButtonType().Danger, label=" All Healer Ranks! ", custom_id="b_all_heal"),
                               Button(style=ButtonType().Secondary, label=" All Tank Ranks! ",
                                      custom_id="b_all_tank", )])])


client.run(TOKEN)
