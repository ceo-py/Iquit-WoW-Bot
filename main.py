import discord
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
from validations.validations import Validation, os
from discord.ext import commands, tasks

SEASON = 2
EXPANSION = "DF"


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(command_prefix="!", help_command=None, intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(ButtonsCharacterStatistics())
        self.add_view(AddCharacterButton())


client = PersistentViewBot()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Waiting for Sunset"))
    print("Ready")


async def backup_message(ctx, embed, characters_information: list):
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/983670671647313930/1056581663230021822/"
        "kisspng-road-signs-in-singapore-warning-sign-traffic-sign-caution-signs-5a8b35b0afe937."
        "9224424515190726887205.png"
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
            url="https://cdn.discordapp.com/attachments/983670671647313930/1056575707259613204/Winners-podium-on-transparent-background-PNG.png"
        )

        data_db = await char_info.get_data_for_rank(cnl_id, None)
        if not data_db:
            data_db = await char_info.get_data_for_rank(cnl_id, "Yes")
            return await backup_message(ctx, embed, data_db)

        total = char_display.get_all_chars(char_display.sorting_db(data_db, "Total"))

        top_cut_offs = "\n".join(
            f"{name} - {rating:.1f}" for rating, name in get_wow_cutoff()
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
        if data_db:
            await compere_char_now_with_db(data_db, cnl_id, db_)


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
                name="Vault of the Incarnates",
                value=f"{c_raid_normal} / 8",
                inline=True,
            )
            embed.add_field(name="Heroic", value=f"{c_raid_heroic} / 8", inline=True)
            embed.add_field(name="Mythic", value=f"{c_raid_mythic} / 8", inline=True)
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
    if data:
        await ctx.send("\n".join(data))


@tasks.loop(seconds=0)
async def task_loop():
    try:
        all_channels_ids = get_all_channels_id(client)

        for id_channel in all_channels_ids:

            data_db = await char_info.get_data_for_rank(id_channel, None)

            if not data_db:
                data_db = await char_info.get_data_for_rank(id_channel, None)

                if not data_db:
                    data_db = await char_info.get_data_for_rank(id_channel, "Yes")

            if not data_db:
                continue

            result = await compere_char_now_with_db(data_db, id_channel, db_)
            ctx = client.get_channel(int(id_channel))
            await show_updated_characters(ctx, [x["output"] for x in result])
    except Exception as e:
        print(e)


@client.command()
async def update(ctx, time_value):
    try:
        if str(ctx.author) == os.getenv("OWNER"):
            task_loop.change_interval(hours=float(time_value))
            if task_loop.next_iteration:
                task_loop.cancel()
            await ctx.send(
                f"```It's set on every {time_value}h to check if there is rating change on every character in the server!```"
            )
            task_loop.start()
    except Exception as e:
        print(e)


@client.command()
async def help(ctx):
    cnl_id = await Validation.msg_check(ctx)
    if cnl_id:
        embed = discord.Embed(
            title="Help Center For Iquit Commands", colour=discord.Colour.blue()
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/880059629252534292/880060565190500423/iq.png"
        )
        embed.add_field(
            name="**!check region realm character name**",
            value="[Example](https://cdn.discordapp.com/attachments/880059629252534292/880077926505250846"
            "/check.png)\n `!check eu draenor ceomerlin` with this command "
            "you are going to see that character current progress in raids, raider IO, last timed "
            "key and more.\n :arrow_down: ",
            inline=False,
        )
        embed.add_field(
            name="**!add**",
            value="[Example](https://cdn.discordapp.com/attachments/983670671647313930/1055864102142083154/image.png)\n"
            "In the popup menu add the needed information. Correct format is region, realm, "
            "character name, your nick name, character class. That character will enter into the rank system "
            "where you can see where you rank compere to your friends and other people that you add to the server database."
            " \n :arrow_down: ",
            inline=False,
        )
        embed.add_field(
            name="**!rank**",
            value="[Example](https://cdn.discordapp.com/attachments/880059629252534292/880064020525223956"
            "/rank.png)\n `!rank` with that command every character that "
            "you add already to the list with `!cadd` command will be compere and ranked by raider "
            "IO with total section dont matter the role and separate "
            " ranks for DPS, Healers and Tanks.\n :arrow_down: ",
            inline=False,
        )
        embed.add_field(
            name="**!token region**",
            value="[Example](https://cdn.discordapp.com/attachments/880059629252534292/880153278111961108"
            "/token.png)\n `!token eu`, `!token us`, `!token china`, `!token korea`, `!token taiwan` "
            " with that command you can check token prices in every region.\n :arrow_down: ",
            inline=False,
        )
        embed.add_field(
            name="**!weather city**",
            value="[Example](https://cdn.discordapp.com/attachments/880059629252534292/880154617730703390"
            "/weather.png)\n `!weather sofia` "
            "with that command you can check the weather in your city or where you want.\n "
            ":arrow_down: ",
            inline=False,
        )
        embed.add_field(
            name="**!ask question**",
            value="[Example](https://cdn.discordapp.com/attachments/880059629252534292/880155463759581194"
            "/ask.png)\n `!ask 2+2`, `!ask capital bulgaria`, `!ask next nba game` "
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
        t, t_min, t_max, feels_like, type_of_weather = weather_check(arg1)
        embed = discord.Embed(
            title=f"Temperature in {arg1.capitalize()} is {t} °C",
            colour=discord.Colour.blue(),
        )
        embed.set_thumbnail(
            url="https://flyclipart.com/downloadpage/images/sun-png-transparent-background-transparent-sun-transparent-375282.png/375282"
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
