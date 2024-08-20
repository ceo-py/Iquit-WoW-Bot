from settings import TOKEN_BASE_URL
from requests_html import HTMLSession

def get_info_token(region) -> tuple:
    # data_ = realms_data[region.lower()]
    # region, flag_region = data_
    session = HTMLSession()

    htmldata = session.get(f"{TOKEN_BASE_URL}{region}")

    price = htmldata.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[1]/div[2]/div/div[1]/div[2]', first=True).text
    change = htmldata.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[1]/div[2]/div/div[2]/div[1]', first=True).text
    three_day_low = htmldata.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[3]/div[2]/table[1]/tbody/tr[1]/td[2]/div/span',
        first=True).text
    seven_day_low = htmldata.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[3]/div[2]/table[1]/tbody/tr[1]/td[3]/div/span',
        first=True).text
    thirty_day_low = htmldata.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[3]/div[2]/table[1]/tbody/tr[1]/td[4]/div/span',
        first=True).text
    three_day_high = htmldata.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[3]/div[2]/table[1]/tbody/tr[2]/td[2]/div/span',
        first=True).text
    seven_day_high = htmldata.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[3]/div[2]/table[1]/tbody/tr[2]/td[3]/div/span',
        first=True).text
    thirty_day_high = htmldata.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[3]/div[2]/table[1]/tbody/tr[2]/td[4]/div/span',
        first=True).text


    return (
        price,
        change,
        three_day_low,
        seven_day_low,
        thirty_day_low,
        three_day_high,
        seven_day_high,
        thirty_day_high,
        flag_region,
    )