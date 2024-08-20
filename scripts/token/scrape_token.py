import time
from requests_html import HTMLSession
from settings import TOKEN_BASE_URL

def timed_cache(ttl):
    """
    Decorator function that implements a timed cache for the decorated function.

    Args:
        ttl (int): Time-to-live in seconds for cached entries.

    Returns:
        function: Decorated function with caching behavior.
    """
    def decorator(func):
        cache = {}

        def wrapper(region):
            current_time = time.time()
            if region in cache:
                timestamp, data = cache[region]
                if (current_time - timestamp) < ttl:
                    return data
            # Call the function and update cache
            data = func(region)
            cache[region] = (current_time, data)
            return data
        return wrapper
    return decorator


@timed_cache(ttl=3600)
def fetch_info_token(region) -> tuple:
    """
    Fetches token information for a given region from a web page.

    Args:
        region (str): The region code to fetch information for.

    Returns:
        tuple: A tuple containing the following information:
            - price (str): Current token price.
            - change (str): Price change.
            - three_day_low (str): 3-day low price.
            - seven_day_low (str): 7-day low price.
            - thirty_day_low (str): 30-day low price.
            - three_day_high (str): 3-day high price.
            - seven_day_high (str): 7-day high price.
            - thirty_day_high (str): 30-day high price.
            - flag_region (str): Region flag emoji.
    """
    flag_region = f":flag_{region.lower()}:"

    session = HTMLSession()
    html_data = session.get(f"{TOKEN_BASE_URL}{region}")

    price = html_data.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[1]/div[2]/div/div[1]/div[2]', first=True).text
    change = html_data.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[1]/div[2]/div/div[2]/div[1]', first=True).text
    three_day_low = html_data.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[3]/div[2]/table[1]/tbody/tr[1]/td[2]/div/span',
        first=True).text
    seven_day_low = html_data.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[3]/div[2]/table[1]/tbody/tr[1]/td[3]/div/span',
        first=True).text
    thirty_day_low = html_data.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[3]/div[2]/table[1]/tbody/tr[1]/td[4]/div/span',
        first=True).text
    three_day_high = html_data.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[3]/div[2]/table[1]/tbody/tr[2]/td[2]/div/span',
        first=True).text
    seven_day_high = html_data.html.xpath(
        '//*[@id="__next"]/div[1]/main/div/div/section[1]/div/div/div[3]/div[2]/table[1]/tbody/tr[2]/td[3]/div/span',
        first=True).text
    thirty_day_high = html_data.html.xpath(
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
        flag_region
    )