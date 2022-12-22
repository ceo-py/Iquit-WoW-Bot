import discord
import os
from dotenv import load_dotenv
from other_commands import weather_check, ask_question, get_info_token, get_affixes, get_wow_cutoff
from data_base_info import DataBaseInfo
from character_info import CharacterInfo
from sorting_ranks import RankCharacterDisplay
from discord.ext import commands

SEASON = 1
EXPANSION = "DF"
char_db = DataBaseInfo()
char_info = CharacterInfo()
char_display = RankCharacterDisplay()
intents = discord.Intents.all()
load_dotenv()
TOKEN = os.getenv("TOKEN")
DISCORD_CHANNEL_NAME = "iquit-bot"


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="?", help_command=None, intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(Buttons())


client = PersistentViewBot()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Waiting for Sunset'))
    print("Ready")


@client.command()
async def rank(ctx):
    cnl_id = await msg_check(ctx)
    if cnl_id:
        embed = discord.Embed(
            title=f"Mythic+ Rankings {EXPANSION} Season {SEASON} - Leaderboard",
            colour=discord.Colour.blue()
        )
        embed.set_thumbnail(url="https://graphly.io/wp-content/uploads/leaderboards-podium-star.jpg")

        data_db = await char_info.get_data_for_rank(cnl_id)

        total = char_display.get_all_chars(char_display.sorting_db(data_db, "Total"))
        top_cut_offs = "\n".join(f"{name} - {rating:.1f}" for rating, name in get_wow_cutoff())
        embed.add_field(name="**Mythic+ Rating Cutoffs**",
                        value=f"```"
                              f"{top_cut_offs}```", inline=False)

        embed.add_field(name="**:regional_indicator_t::regional_indicator_o::regional_indicator_p: :nine:**",
                        value=f"{total[1]}\n{total[2]}\n"
                              f"{total[3]}", inline=True)
        embed.add_field(name=":arrow_down_small:",
                        value=f"{total[4]}\n{total[5]}\n{total[6]}",
                        inline=True)
        embed.add_field(name=":arrow_down_small:",
                        value=f"{total[7]}\n{total[8]}\n{total[9]}",
                        inline=True)
        embed.add_field(name=":regional_indicator_t::regional_indicator_o::regional_indicator_p: :three:",
                        value="**Ranking by roles:**", inline=False)
        dps = char_display.get_other_ranks(char_display.sorting_db(data_db, "DPS"), "DPS")
        embed.add_field(name=":crossed_swords:",
                        value=f":first_place:{dps[1]}\n:second_place:{dps[2]}\n:third_place:{dps[3]}",
                        inline=True)

        heal = char_display.get_other_ranks(char_display.sorting_db(data_db, "Heal"), "Heal")
        embed.add_field(name=":heart:",
                        value=f":first_place:{heal[1]}\n:second_place:{heal[2]}\n:third_place:{heal[3]}",
                        inline=True)

        tank = char_display.get_other_ranks(char_display.sorting_db(data_db, "Tank"), "Tank")
        embed.add_field(name=":shield:",
                        value=f":first_place:{tank[1]}\n:second_place:{tank[2]}\n:third_place:{tank[3]}",
                        inline=True)
        embed.add_field(name="This Week Affixes",
                        value=f"[**{get_affixes()}**](https://mplus.subcreation.net/index.html)", inline=False)
        embed.add_field(name="World Top Ranks",
                        value=f"[**Mythic+ Rankings for All Classes & Roles ({EXPANSION} Season {SEASON})**]("
                              f"https://raider.io/mythic-plus-character-rankings/season-{EXPANSION.lower()}-{SEASON}/world/all/all)\n "
                              f"[**Mythic+ Rankings for All Tanks ({EXPANSION} Season {SEASON})**]("
                              f"https://raider.io/mythic-plus-character-rankings/season-{EXPANSION.lower()}-{SEASON}/world/all/tank)\n "
                              f"[**Mythic+ Rankings for All Healers ({EXPANSION} Season {SEASON})**]("
                              f"https://raider.io/mythic-plus-character-rankings/season-{EXPANSION.lower()}-{SEASON}/world/all/healer)\n "
                              f"[**Mythic+ Rankings for All DPS ({EXPANSION} Season {SEASON})**]("
                              f"https://raider.io/mythic-plus-character-rankings/season-{EXPANSION.lower()}-{SEASON}/world/all/dps)",
                        inline=False)
        view = Buttons()
        await ctx.send(embed=embed, view=view)


@client.command()
async def check(ctx, *args):
    cnl_id = await msg_check(ctx)
    if cnl_id:
        try:
            tmbn, name, spec, c, cname, ilvl, class_icon, tank, dps, healer, c_raid_normal, c_raid_heroic, c_raid_mythic, lfinish, keylevel, \
            keyup, rscore, player_region, player_realm, player_name, score, purl = await char_info.check_single_character(
                args, cnl_id)
            embed = discord.Embed(
                title=str(score) + " - Best Mythic+ Score",
                description=f"[Character Link]({purl}) :link: "f"[Armory Profile](https://worldofwarcraft.com/en-{player_region}/character/{player_region}/{player_realm}/{player_name})\n"
                            f"[Simulate on RaidBots](https://www.raidbots.com/simbot/quick?region={player_region}&realm={player_realm}&name={player_name}) :link: "
                            f"[Warcraft Logs Profile](https://www.warcraftlogs.com/character/{player_region}/{player_realm}/{player_name})",
                colour=discord.Colour.blue()
            )
            embed.set_thumbnail(url=tmbn)
            embed.set_author(name=f'{name}, {spec}, {c}, {cname}, {ilvl} ILVL', icon_url=class_icon)
            embed.add_field(name=":shield:", value=tank, inline=True)
            embed.add_field(name=":crossed_swords:", value=dps, inline=True)
            embed.add_field(name=":green_heart:", value=healer, inline=True)
            embed.add_field(name="Vault of the Incarnates", value=f"{c_raid_normal} / 8", inline=True)
            embed.add_field(name="Heroic", value=f"{c_raid_heroic} / 8", inline=True)
            embed.add_field(name="Mythic", value=f"{c_raid_mythic} / 8", inline=True)
            embed.add_field(name="Last Finished Dungeon", value=f"{lfinish}", inline=False)
            embed.add_field(name="Key Level", value=f"{keylevel}", inline=True)
            embed.add_field(name="Key Upgrade", value=f"{keyup}", inline=True)
            embed.add_field(name="Points", value=f"{rscore}", inline=True)
            embed.add_field(name="Current Affixes",
                            value=f"[**{get_affixes()}**](https://mplus.subcreation.net/index.html)", inline=False)
            await ctx.send(embed=embed)
        except TypeError:
            await ctx.send(
                "Not valid information, check what you type! The Right format is `region` `realm` `character name` or `character nickname` `class`."
                "You can use `!help` for more information or check the examples below:"
                "```!check eu draenor ceomerlin```"
                "```!check ceo warlock```"
                "second example can be used if character is already in the data base if its not use the first one!")


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
        t, t_min, t_max, feels_like, type_of_weather = weather_check(arg1)
        embed = discord.Embed(
            title=f"Temperature in {arg1.capitalize()} is {t} °C",
            colour=discord.Colour.blue()
        )
        embed.set_thumbnail(
            url="https://flyclipart.com/downloadpage/images/sun-png-transparent-background-transparent-sun-transparent-375282.png/375282")
        embed.add_field(name=f"Feels {type_of_weather}", value=f"{feels_like} °C", inline=False)
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


class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="All Total Rank!", style=discord.ButtonStyle.blurple, custom_id="1")
    async def total(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message(
            f"```TOP Total\n{await button_info_display('Total', str(button.channel.id))}```", ephemeral=True)

    @discord.ui.button(label="All Dps Ranks!", style=discord.ButtonStyle.green, custom_id="2")
    async def dps(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message(
            f"```TOP DPS\n{await button_info_display('DPS', str(button.channel.id))}```", ephemeral=True)

    @discord.ui.button(label="All Healer Ranks!", style=discord.ButtonStyle.red, custom_id="3")
    async def heal(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message(
            f"```TOP Healers\n{await button_info_display('Heal', str(button.channel.id))}```", ephemeral=True)

    @discord.ui.button(label="All Tank Ranks!", style=discord.ButtonStyle.gray, custom_id="4")
    async def tank(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message(
            f"```TOP Tanks\n{await button_info_display('Tank', str(button.channel.id))}```", ephemeral=True)


async def button_info_display(type_of_info, channel_id):
    data_db = await char_info.get_data_for_rank(channel_id)
    data_db = char_display.sorting_db(data_db, f"{type_of_info}")
    return char_display.button_rank_result(data_db, f"{type_of_info}")


client.run(TOKEN)
