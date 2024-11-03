from utils.token.get_battle_net_token import get_battle_net_token
from settings import BATTLE_CLIENT_ID, BATTLE_CLIENT_SECRET, BATTLE_NET_AUTH_URL
import requests


def generate_url_token_api(region: str) -> str:
    battle_net_token = get_battle_net_token(
        BATTLE_CLIENT_ID, BATTLE_CLIENT_SECRET, BATTLE_NET_AUTH_URL
    )
    return f"https://{region}.api.blizzard.com/data/wow/token/index?namespace=dynamic-{region}&locale=en_{region.capitalize()}&access_token={battle_net_token}"


async def get_token_price(region: str) -> int:
    url = generate_url_token_api(region)
    with requests.get(url) as response:
        if response.status_code == 200:
            return response.json()["price"] / 10000

    return 0
