import requests
import os
from requests_html import HTMLSession
from dotenv import load_dotenv

load_dotenv()


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
    realms_data = {
        "us": ["US", ":flag_us:"],
        "eu": ["EU", ":flag_eu:"],
        "china": ["China", ":flag_cn:"],
        "korea": ["Korea", ":flag_kr:"],
        "taiwan": ["Taiwan", ":flag_tw:"],
    }
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


def get_wow_cutoff():
    with requests.get(
        f"""https://raider.io/api/v1/mythic-plus/season-cutoffs?season=season-df-1&region=eu"""
    ) as x:
        data = x.json()
        top0_1 = data["cutoffs"]["graphData"]["p999"]["data"][0]["y"]
        top0_1_name = data["cutoffs"]["graphData"]["p999"]["name"]
        top1 = data["cutoffs"]["graphData"]["p990"]["data"][0]["y"]
        top1_name = data["cutoffs"]["graphData"]["p990"]["name"]
        top10 = data["cutoffs"]["graphData"]["p900"]["data"][0]["y"]
        top10_name = data["cutoffs"]["graphData"]["p900"]["name"]
    return (top0_1, top0_1_name), (top1, top1_name), (top10, top10_name)


def emojis(char_name: str) -> str:
    emojis_data = {
        "evoker": "<:evoker:1058463307348054087>",
        "warrior": "<:warrior:1058463593617703034>",
        "shaman": "<:shaman:1058463886707273729>",
        "demon hunter": "<:demonhunter:1058464098758693034>",
        "warlock": "<:warlock:1058464246092005456>",
        "druid": "<:druid:1058464381622558910>",
        "mage": "<:mage:1058464565379211304>",
        "death knight": "<:deathknight:1058464682542903418>",
        "rouge": "<:rogue:1058464885790482593>",
        "hunter": "<:hunter:1058464998046838834>",
        "paladin": "<:paladin:1058465116477214893>",
        "priest": "<:priest:1058465325877842032>",
        "monk": "<:monk:1058465435957338192>",
        "tank": "<:Tankrole:1058479529158529124>",
        "healer": "<:Healerrole:1058479567616090222>",
        "dps": "<:DPSrole:1058479594438668468>",
        "total": "<:Totalrole:1058488589459136512>",
    }
    return emojis_data.get(char_name, "None")


async def compere_char_now_with_db(data: list, id_channel: str, db) -> list:
    result = []
    for show in data:
        char_db_information = await db.find_character_in_db(
            id_channel, Character_Name=show["Character Name"].lower()
        )

        if show["Total"] > char_db_information["Total Rating"]:
            result.append(
                {
                    "output": f"{emojis(char_db_information['Class to display'])} **{show['Character Name'].capitalize()}** gain {abs(show['Total'] - char_db_information['Total Rating'])} "
                    f"rating reaching **__{show['Total']}__** !",
                    "score": abs(show["Total"] - char_db_information["Total Rating"]),
                }
            )
            show.popitem()
            await db.update_character_info(id_channel, *show.values())

    return sorted(result, key=lambda x: -x["score"])


def get_all_channels_id(client) -> list:
    return [
        channel.id
        for server in client.guilds
        for channel in server.channels
        if channel.name == os.getenv("DISCORD_CHANNEL_NAME")
    ]
