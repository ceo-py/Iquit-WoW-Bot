import requests
import os
from requests_html import HTMLSession
from dotenv import load_dotenv
load_dotenv()


def weather_check(arg):
    with requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={arg}&appid={os.getenv('API_WEATHER')}&units=metric"
    ) as x:
        t = format(x.json().get("main").get('temp'), ".1f")
        t_min = format(x.json().get("main").get('temp_min'), ".0f")
        t_max = format(x.json().get("main").get('temp_max'), ".0f")
        feels_like = format(x.json().get("main").get('feels_like'), ".1f")
        return t, t_min, t_max, feels_like


def ask_question(args):
    query = '+'.join(args)
    with requests.get(
            f"https://api.wolframalpha.com/v1/result?appid={os.getenv('API_ASK_Q')}={query}%3F") as response:
        return response.status_code, response.text


def get_info_token(region):
    realms_data = {"us": ["US", ":flag_us:"], "eu": ["EU", ":flag_eu:"], "china": ["China", ":flag_cn:"],
                   "korea": ["Korea", ":flag_kr:"], "taiwan": ["Taiwan", ":flag_tw:"]}
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
    return price, change, one_day_low, seven_day_low, thirty_day_low, one_day_high, \
           seven_day_high, thirty_day_high, flag_region


# change region for afix eu us etc..
def get_affixes():
    with requests.get(
            f'''https://raider.io/api/v1/mythic-plus/affixes?region=eu&locale=en''') as af:
        return af.json().get('title')
