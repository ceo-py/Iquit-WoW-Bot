import datetime
import discord
from discord import app_commands
from buttons.button_add_character import AddCharacterButton
from buttons.buttons_stats_total_dps_heal_tank import (
    ButtonsCharacterStatistics,
    char_info,
    char_display,
    db_,
)
from other_commands import (
    weather_check,
    ask_question,
    get_info_token,
    get_affixes,
    get_wow_cutoff,
    compere_char_now_with_db,
    emojis,
    get_all_channels_id,
)
from tree_commands.rank import TreeCommands as TC
from tree_commands.validation import ValidationTreeCommands as VTC
from validations.validations import Validation, os
from discord.ext import commands, tasks

SEASON = 4
EXPANSION = "DF"

UTC = datetime.timezone.utc
times = [datetime.time(hour=x) for x in range(0, 24, 2)]


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(command_prefix="!", help_command=None, intents=intents)

    async def on_ready(self):
        self.scheduler_rio_every_2_hours.start()
        # await client.tree.sync() # once only to sync CRUD slash command
        await self.change_presence(activity=discord.Game(name="Waiting for Sunset"))
        print("Ready")

    def scheduler_rio_every_2_hours_unload(self):
        self.scheduler_rio_every_2_hours.cancel()

    @tasks.loop(time=times)
    async def scheduler_rio_every_2_hours(self):
        try:
            all_channels_ids = get_all_channels_id(self)

            custom_channels = {
                int(x["custom id"]): int(x["db channel id"])
                for x in list(db_.custom_channels_ids().find())
            }

            if custom_channels:
                all_channels_ids.update(custom_channels)
                all_channels_ids = TC.remove_channels(all_channels_ids, custom_channels)

            for ctx_msg, id_channel in all_channels_ids.items():

                data_db = await char_info.get_data_for_rank(id_channel, None)

                if not data_db:
                    data_db = await char_info.get_data_for_rank(id_channel, None)

                    if not data_db:
                        data_db = await char_info.get_data_for_rank(id_channel, "Yes")

                if not data_db:
                    continue

                result = await compere_char_now_with_db(data_db, id_channel, db_)
                ctx = self.get_channel(int(ctx_msg))
                if ctx and result:
                    await show_updated_characters(ctx, [x["output"] for x in result])
        except Exception as e:
            print(f"scheduler_rio_every_2_hours - {e}")

    async def setup_hook(self) -> None:
        self.add_view(ButtonsCharacterStatistics())
        self.add_view(AddCharacterButton())


client = PersistentViewBot()


# @client.event
# async def on_ready():
#     # await client.tree.sync() # once only to sync CRUD slash command
#     await client.change_presence(activity=discord.Game(name="Waiting for Sunset"))
#     print("Ready")


async def backup_message(ctx, embed, characters_information: list):
    embed.set_thumbnail(
        url="https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/caution_icon.png?raw=true"
    )
    total = char_display.get_all_chars(
        char_display.sorting_db(characters_information, "Total")
    )

    embed.add_field(
        name="**This is backup version**",
        value=f"```" f"Raider IO is not working at the moment```",
        inline=False,
    )

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
    await ctx.send(embed=embed)


@client.command()
async def rank(ctx):
    cnl_id = await Validation.msg_check(ctx)
    if cnl_id:
        embed = discord.Embed(
            title=f"Mythic+ Rankings {EXPANSION} Season {SEASON} - Leaderboard",
            colour=discord.Colour.blue(),
        )
        embed.set_thumbnail(
            url="https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/rank_command_thumb.png?raw=true"
        )

        data_db = await char_info.get_data_for_rank(cnl_id, None)
        if data_db == 'Error':
            data_db = await char_info.get_data_for_rank(cnl_id, "Yes")
            return await backup_message(ctx, embed, data_db)

        total = char_display.get_all_chars(char_display.sorting_db(data_db, "Total"))

        region = await db_.get_region(cnl_id)

        if region:
            top_cut_offs = "\n".join(
                f"{name} - {rating:.1f}" for rating, name in get_wow_cutoff(region, SEASON)
            )
            embed.add_field(
                name="**Mythic+ Rating Cutoffs**",
                value=f"```" f"{top_cut_offs}```",
                inline=False,
            )

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
        view = ButtonsCharacterStatistics()
        await ctx.send(embed=embed, view=view)
        await compere_char_now_with_db(data_db, cnl_id, db_)


@client.tree.command(
    name="ranksimple", description="Show top-rated players for a specific role."
)
async def ranksimple(interaction: discord.Interaction, role: TC.roles(), top: TC.top()):
    if not interaction.guild:
        await interaction.response.send_message(
            "**This command can only be used in a server text channel.**"
        )
        return

    players = await TC.get_players(interaction, os.getenv("DISCORD_CHANNEL_NAME"), role)
    output = TC.generate_output(*players, top)
    await TC.message_respond_interaction(interaction, top, role, output)


class RankSimpleLoop:
    def __init__(self, role, top):

        self.top = top
        self.role = role

    @tasks.loop()
    async def loop_simple(self, interaction):
        try:
            players = await TC.get_players(
                interaction, os.getenv("DISCORD_CHANNEL_NAME"), self.role
            )
            output = TC.generate_output(*players, self.top)
            ctx = client.get_channel(int(interaction.channel.id))
            await TC.message_respond_ctx(ctx, self.top, self.role, output)
        except Exception as e:
            print(f"loop_simple {e}")


@client.tree.command(
    name="ranksimpleloop", description=f"Scheduled daily run. NB Server Time UTC!!!"
)
@app_commands.describe(hour=f"Hour range: 1-24.")
@app_commands.describe(minute=f"Minute range: 0-59.")
async def ranksimpleloop(
        interaction: discord.Interaction,
        hour: int,
        minute: int,
        role: TC.roles(),
        top: TC.top(),
):
    if VTC.hour(hour):
        await interaction.response.send_message(f"Right format for hour is from 1 - 24")
        return

    if VTC.minute(minute):
        await interaction.response.send_message(
            f"Right format for minute is from 0 - 59"
        )
        return

    if not interaction.guild:
        await interaction.response.send_message(
            "**This command can only be used in a server text channel.**"
        )
        return

    rsl = RankSimpleLoop(role, top)
    rsl.loop_simple.change_interval(
        time=datetime.time(hour=hour, minute=minute, tzinfo=datetime.timezone.utc)
    )

    if rsl.loop_simple.next_iteration:
        rsl.loop_simple.cancel()
    rsl.loop_simple.start(interaction)

    await interaction.response.send_message(
        f"**Schedule: TOP {top} {role} results daily at {hour:02}:{minute:02} UTC.**"
    )


@client.tree.command(
    name="rankglobalsetting",
    description="Add/Remove custom channel for global rank announcement.",
)
async def rankglobalsetting(
        interaction: discord.Interaction, option: TC.custom_channel_options()
):
    if not interaction.guild:
        await interaction.response.send_message(
            "**This command can only be used in a server text channel.**"
        )
        return

    output = ""

    if option == "Add":
        main_channel = TC.find_db_channel_id(interaction.guild.channels)
        if not main_channel:
            await interaction.response.send_message(f"You need to create channel named **'iquit-bot'** first!!!")
            return

        output = db_.add_custom_channel(
            interaction.channel_id,
            main_channel,
            interaction.channel.name,
        )

    elif option == "Remove":
        output = db_.skip_custom_channel(
            interaction.channel_id, interaction.channel.name
        )

    await interaction.response.send_message(output)


@client.command()
async def check(ctx, *args):
    cnl_id = await Validation.msg_check(ctx)
    if cnl_id:
        try:
            (
                tmbn,
                name,
                spec,
                c,
                cname,
                ilvl,
                class_icon,
                tank,
                dps,
                healer,
                c_raid_normal,
                c_raid_heroic,
                c_raid_mythic,
                lfinish,
                keylevel,
                keyup,
                rscore,
                player_region,
                player_realm,
                player_name,
                score,
                purl,
                total_bosses,
            ) = await char_info.check_single_character(args, cnl_id)
            embed = discord.Embed(
                title=str(score) + " - Best Mythic+ Score",
                description=f"[Character Link]({purl}) :link: "
                            f"[Armory Profile](https://worldofwarcraft.com/en-{player_region}/character/{player_region}/{player_realm}/{player_name})\n"
                            f"[Simulate on RaidBots](https://www.raidbots.com/simbot/quick?region={player_region}&realm={player_realm}&name={player_name}) :link: "
                            f"[Warcraft Logs Profile](https://www.warcraftlogs.com/character/{player_region}/{player_realm}/{player_name})",
                colour=discord.Colour.blue(),
            )
            embed.set_thumbnail(url=tmbn)
            embed.set_author(
                name=f"{name}, {spec}, {c}, {cname}, {ilvl} ILVL", icon_url=class_icon
            )
            embed.add_field(name=":shield:", value=tank, inline=True)
            embed.add_field(name=":crossed_swords:", value=dps, inline=True)
            embed.add_field(name=":green_heart:", value=healer, inline=True)
            embed.add_field(
                name="Amirdrassil, the Dream's Hope",
                value=f"{c_raid_normal} / {total_bosses}",
                inline=True,
            )
            embed.add_field(name="Heroic", value=f"{c_raid_heroic} / {total_bosses}", inline=True)
            embed.add_field(name="Mythic", value=f"{c_raid_mythic} / {total_bosses}", inline=True)
            embed.add_field(
                name="Last Finished Dungeon", value=f"{lfinish}", inline=False
            )
            embed.add_field(name="Key Level", value=f"{keylevel}", inline=True)
            embed.add_field(name="Key Upgrade", value=f"{keyup}", inline=True)
            embed.add_field(name="Points", value=f"{rscore}", inline=True)
            embed.add_field(
                name="Current Affixes",
                value=f"[**{get_affixes()}**](https://mplus.subcreation.net/index.html)",
                inline=False,
            )
            await ctx.send(embed=embed)
        except TypeError:
            await ctx.send(
                "Not valid information, check what you type! The Right format is `region` `realm` `character name` or `character nickname` `class`."
                "You can use `!help` for more information or check the examples below:"
                "```!check eu draenor ceomerlin```"
                "```!check ceo warlock```"
                "second example can be used if character is already in the data base if its not use the first one!"
            )


@client.command()
async def add(ctx):
    cnl_id = await Validation.msg_check(ctx)
    if cnl_id:
        await ctx.send(view=AddCharacterButton())


async def show_updated_characters(ctx, data: list) -> None:
    if data and ctx:
        for msg in data:
            await ctx.send(msg)


# @tasks.loop(seconds=0)
# async def task_loop():
#     try:
#         all_channels_ids = get_all_channels_id(client)
#         custom_channels = list(db_.custom_channels_ids().find())
#
#         custom_channels = {
#             int(x["custom id"]): int(x["db channel id"])
#             for x in list(db_.custom_channels_ids().find())
#         }
#
#         if custom_channels:
#             all_channels_ids.update(custom_channels)
#             all_channels_ids = TC.remove_channels(all_channels_ids, custom_channels)
#
#         for ctx_msg, id_channel in all_channels_ids.items():
#             if id_channel != 1053417781879644191:
#                 continue
#
#             data_db = await char_info.get_data_for_rank(id_channel, None)
#
#             if not data_db:
#                 data_db = await char_info.get_data_for_rank(id_channel, None)
#
#                 if not data_db:
#                     data_db = await char_info.get_data_for_rank(id_channel, "Yes")
#
#             if not data_db:
#                 continue
#
#             result = await compere_char_now_with_db(data_db, id_channel, db_)
#
#             ctx = client.get_channel(int(ctx_msg))
#             await show_updated_characters(ctx, [x["output"] for x in result])
#     except Exception as e:
#         print(f"task_loop - {e}")


# @client.command()
# async def update(ctx, time_value):
#     try:
#         if str(ctx.author) == os.getenv("OWNER"):
#             task_loop.change_interval(hours=float(time_value))
#             if task_loop.next_iteration:
#                 task_loop.cancel()
#             await ctx.send(
#                 f"```It's set on every {time_value}h to check if there is rating change on every character in the server!```"
#             )
#             task_loop.start()
#     except Exception as e:
#         print(e)


@client.command()
async def delete_character(ctx, character_name):
    cnl_id = await Validation.msg_check(ctx)
    if cnl_id:
        await ctx.send(await db_.delete_user_from_db(cnl_id, character_name))


@client.command()
async def help(ctx):
    cnl_id = await Validation.msg_check(ctx)
    if cnl_id:
        embed = discord.Embed(
            title="Help Center For Iquit Commands", colour=discord.Colour.blue()
        )
        embed.set_thumbnail(
            url="https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/iquit_text.png?raw=true"
        )
        embed.add_field(
            name="**!check region realm character name**",
            value="[Example](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/"
                  "check_command_example.png?raw=true)\n `!check eu tarren-mill Naowhlul` with this command "
                  "you are going to see that character current progress in raids, raider IO, last timed "
                  "key and more.\n :arrow_down: ",
            inline=False,
        )
        embed.add_field(
            name="**!add**",
            value="[Example](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/add_character_modal.png?raw=true)\n"
                  "In the popup menu add the needed information. Correct format is region, realm, "
                  "character name, your nick name, character class. That character will enter into the rank system "
                  "where you can see where you rank compere to your friends and other people that you add to the server database."
                  " \n :arrow_down: ",
            inline=False,
        )
        embed.add_field(
            name="**!rank**",
            value="[Example](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/"
                  "rank_command_example.png?raw=true)\n `!rank` with that command every character that "
                  "you add already to the list with `!cadd` command will be compere and ranked by raider "
                  "IO with total section dont matter the role and separate "
                  " ranks for DPS, Healers and Tanks.\n :arrow_down: ",
            inline=False,
        )
        embed.add_field(
            name="**!delete_character character name**",
            value="[Example](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/"
                  "delete_command_example.png?raw=true)\n `!delete_character Klirik` with that command if the character exist in the channel "
                  "database it will be delete. You can add it anytime using the add button.\n :arrow_down: ",
            inline=False,
        )
        embed.add_field(
            name="**!token region**",
            value="[Example](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/"
                  "toke_price_example.png?raw=true)\n `!token eu`, `!token us`, `!token china`, `!token korea`, `!token taiwan` "
                  " with that command you can check token prices in every region.\n :arrow_down: ",
            inline=False,
        )
        embed.add_field(
            name="**!weather city**",
            value="[Example](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/weather_example.png?raw=true)"
                  "\n `!weather dallas` "
                  "with that command you can check the weather in your city or where you want.\n "
                  ":arrow_down: ",
            inline=False,
        )
        embed.add_field(
            name="**!ask question**",
            value="[Example](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/"
                  "ask_command_example.png?raw=true)\n `!ask 2+2`, `!ask capital bulgaria`, `!ask next nba game` "
                  "with that command you can ask simple questions like you ask your google or amazon "
                  "assistance.",
            inline=False,
        )
        await ctx.send(embed=embed)


@client.command()
async def weather(ctx, arg1=None):
    cnl_id = await Validation.msg_check(ctx)
    if cnl_id:
        if arg1 is None:
            await ctx.send(f"Make sure you type town name.\nExample **!weather Sofia**")
            return
        t, t_min, t_max, feels_like, type_of_weather, weather_icon = weather_check(arg1)
        embed = discord.Embed(
            title=f"Temperature in {arg1.capitalize()} is {t} °C",
            colour=discord.Colour.blue(),
        )
        # embed.set_thumbnail(
        #     url="https://flyclipart.com/downloadpage/images/sun-png-transparent-background-transparent-sun-transparent-375282.png/375282"
        # )
        embed.set_thumbnail(
            url=f"https://openweathermap.org/img/wn/{weather_icon}@2x.png"
        )
        embed.add_field(
            name=f"Feels {type_of_weather}", value=f"{feels_like} °C", inline=False
        )
        embed.add_field(name="Min Temperature : ", value=f"{t_min} °C", inline=True)
        embed.add_field(name="Max Temperature : ", value=f"{t_max} °C", inline=True)
        await ctx.send(embed=embed)


@client.command()
async def ask(ctx, *args):
    cnl_id = await Validation.msg_check(ctx)
    if cnl_id:
        if not args:
            await ctx.send(
                f"Make sure you type your question.\nExample **!ask what is capital of USA**"
            )
            return
        status_code, answer_to_show = ask_question(args)
        if status_code == 501:
            await ctx.send("Meh I`m Stupid don`t know the answer!")
        else:
            embed = discord.Embed(title=answer_to_show, colour=discord.Colour.blue())
            await ctx.send(embed=embed)


@client.command()
async def token(ctx, region=None):
    cnl_id = await Validation.msg_check(ctx)
    if cnl_id:
        if region is None:
            await ctx.send(
                f"Make sure you type right region.\nRegions are: us, eu, china, korea, taiwan\nExample **!token eu**"
            )
            return
        (
            price,
            change,
            one_day_low,
            seven_day_low,
            thirty_day_low,
            one_day_high,
            seven_day_high,
            thirty_day_high,
            flag_region,
        ) = get_info_token(region)
        embed = discord.Embed(
            title=f"**Current Token Price {flag_region} {price} :moneybag:**",
            description=f"**Change {change} :moneybag:**",
            colour=discord.Colour.blue(),
        )
        embed.set_thumbnail(
            url="https://wowtokenprices.com/assets/wowtoken-compressed.png"
        )
        embed.add_field(
            name="**1 DAY**",
            value=f"***Low : {one_day_low} :moneybag:\n"
                  f"High : {one_day_high} :moneybag:***",
            inline=True,
        )
        embed.add_field(
            name="**7 DAY**",
            value=f"***Low : {seven_day_low} :moneybag:\n"
                  f"High : {seven_day_high} :moneybag:***",
            inline=True,
        )
        embed.add_field(
            name="**30 DAY**",
            value=f"***Low : {thirty_day_low} :moneybag:\n"
                  f"High : {thirty_day_high} :moneybag:***",
            inline=True,
        )
        await ctx.send(embed=embed)


client.run(os.getenv("TOKEN"))
