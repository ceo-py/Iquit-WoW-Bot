import requests
import os
from requests_html import HTMLSession
from dotenv import load_dotenv

load_dotenv()

realms_data = {
    "us": ["US", ":flag_us:"],
    "eu": ["EU", ":flag_eu:"],
    "china": ["China", ":flag_cn:"],
    "korea": ["Korea", ":flag_kr:"],
    "taiwan": ["Taiwan", ":flag_tw:"],
}

emojis_data = {
    "evoker": "<:evoker:1058463307348054087>",
    "warrior": "<:warrior:1058463593617703034>",
    "shaman": "<:shaman:1058463886707273729>",
    "demon hunter": "<:demonhunter:1058464098758693034>",
    "warlock": "<:warlock:1058464246092005456>",
    "druid": "<:druid:1058464381622558910>",
    "mage": "<:mage:1058464565379211304>",
    "death knight": "<:deathknight:1058464682542903418>",
    "rogue": "<:rogue:1058464885790482593>",
    "hunter": "<:hunter:1058464998046838834>",
    "paladin": "<:paladin:1058465116477214893>",
    "priest": "<:priest:1058465325877842032>",
    "monk": "<:monk:1058465435957338192>",
    "tank": "<:Tankrole:1058479529158529124>",
    "healer": "<:Healerrole:1058479567616090222>",
    "dps": "<:DPSrole:1058479594438668468>",
    "total": "<:Totalrole:1058488589459136512>",
    "green_arrow": "<a:7636greenarrowup:1065609926149410847>",
    "plus": "<:ezgif:1065614756393783296>",
    "loading": "<a:loading_button:1065596200667066389>",
    "white_arrow_right": "<a:1830vegarightarrow:1065603909147693207>",
    "white_arrow_left": "<a:8826vegaleftarrow:1065603928860925962>",
    "player_add": "<:6332logmemberplusw:1065621500855586907>",
}

pos_description = {1: "st", 2: "nd", 3: "rd"}

db_update_fields = {"Total Rating": "", "DPS": "", "Healer": "", "Tank": ""}

changes_pos = ["rises", "drops"]


def weather_check(arg):
    with requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={arg}&appid={os.getenv('API_WEATHER')}&units=metric"
    ) as x:
        x = x.json()
        t = x["main"]["temp"]
        t_min = x["main"]["temp_min"]
        t_max = x["main"]["temp_max"]
        feels_like = x["main"]["feels_like"]
        type_of_weather = x["weather"][0]["main"]
        return t, t_min, t_max, feels_like, type_of_weather


def ask_question(args):
    query = "+".join(args)
    with requests.get(
        f"https://api.wolframalpha.com/v1/result?appid={os.getenv('API_ASK_Q')}={query}%3F"
    ) as response:
        return response.status_code, response.text


def get_info_token(region):
    data_ = realms_data[region.lower()]
    region, flag_region = data_
    session = HTMLSession()
    htmldata = session.get(f"https://wowtokenprices.com/{region}")
    price = htmldata.html.xpath('//*[@id="money-text"]', first=True).text
    change = htmldata.html.xpath('//*[@id="money-text-small"]', first=True).text
    one_day_low = htmldata.html.xpath('//*[@id="1-day-low"]', first=True).text
    seven_day_low = htmldata.html.xpath('//*[@id="7-day-low"]', first=True).text
    thirty_day_low = htmldata.html.xpath('//*[@id="30-day-low"]', first=True).text
    one_day_high = htmldata.html.xpath('//*[@id="1-day-high"]', first=True).text
    seven_day_high = htmldata.html.xpath('//*[@id="7-day-high"]', first=True).text
    thirty_day_high = htmldata.html.xpath('//*[@id="30-day-high"]', first=True).text
    return (
        price,
        change,
        one_day_low,
        seven_day_low,
        thirty_day_low,
        one_day_high,
        seven_day_high,
        thirty_day_high,
        flag_region,
    )


# change region for afix eu us etc..
def get_affixes():
    with requests.get(
        f"""https://raider.io/api/v1/mythic-plus/affixes?region=eu&locale=en"""
    ) as af:
        return af.json().get("title")


def get_wow_cutoff(region, season):
    with requests.get(
        f"""https://raider.io/api/v1/mythic-plus/season-cutoffs?season=season-df-{season}&region={region}"""
    ) as x:
        try :
            data = x.json()
            top0_1 = data["cutoffs"]["graphData"]["p999"]["data"][0]["y"]
            top0_1_name = data["cutoffs"]["graphData"]["p999"]["name"]
            top1 = data["cutoffs"]["graphData"]["p990"]["data"][0]["y"]
            top1_name = data["cutoffs"]["graphData"]["p990"]["name"]
            top10 = data["cutoffs"]["graphData"]["p900"]["data"][0]["y"]
            top10_name = data["cutoffs"]["graphData"]["p900"]["name"]
        except KeyError as err:
            print(f'There is error with cutoff Request: \n {err}\n{x}')
            return (0, 'No Information'),

    return (top0_1, top0_1_name), (top1, top1_name), (top10, top10_name)


def emojis(char_name: str) -> str:
    return emojis_data.get(char_name, "None")


def sort_api_data_by_total(data):
    return sorted(data, key=lambda x: -x["Total"])


def compere_new_with_current_position(new_pos, current_pos):
    if new_pos > current_pos != 0:
        status = "drops"

    elif new_pos < current_pos or current_pos == 0:
        status = "rises"

    else:
        status = "remains"

    return f'{status} at {new_pos}{pos_description.get(new_pos, "th")} position.'


def merge_data_for_update_db(dict_data: dict, list_data: list) -> dict:
    return {k: v for k, v in zip(dict_data.keys(), list_data)}


async def compere_char_now_with_db(data: list, id_channel: str, db) -> list:
    result = []
    for pos, show in enumerate(sort_api_data_by_total(data), 1):
        char_db_information = await db.find_character_in_db(
            id_channel, Character_Name=show["Character Name"].lower().strip()
        )

        pos_status_str = compere_new_with_current_position(
            pos, char_db_information.get("Position")
        )

        if any([x in pos_status_str for x in changes_pos]):
            await db.update_character_info(
                id_channel, show["Character Name"], {"Position": pos}
            )

        if show.get("Total") > char_db_information.get("Total Rating"):
            result.append(
                {
                    "output": f"{emojis(char_db_information['Class to display'])} "
                    f"**{show['Character Name'].capitalize()}** "
                    f"{emojis('plus')}{abs(show['Total'] - char_db_information['Total Rating'])} "
                    f"rating reaching **__{show['Total']}__**{emojis('green_arrow')} {pos_status_str}"
                }
            )
            show.popitem()
            await db.update_character_info(
                id_channel,
                show.pop("Character Name"),
                merge_data_for_update_db(db_update_fields, show.values()),
            )

    return result


def get_all_channels_id(client) -> list:
    return {
        channel.id: channel.id
        for server in client.guilds
        for channel in server.channels
        if os.getenv("DISCORD_CHANNEL_NAME") in channel.name
    }


def generate_superscript_numbers(numbers):
    numbers_superscript = {
        "0": "⁰",
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹",
    }
    return ("").join(numbers_superscript[x] for x in str(numbers))
