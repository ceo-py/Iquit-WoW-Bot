from utils.token.get_battle_net_token import get_battle_net_token
from settings import BATTLE_CLIENT_ID, BATTLE_CLIENT_SECRET, BATTLE_NET_AUTH_URL
import aiohttp


def generate_url_token_api(region: str) -> str:
    return f"https://{region.lower()}.api.blizzard.com/data/wow/token/?namespace=dynamic-{region.lower()}"


async def get_token_price(region: str) -> int:
    url = generate_url_token_api(region)
    battle_net_token = await get_battle_net_token(
        BATTLE_CLIENT_ID, BATTLE_CLIENT_SECRET, BATTLE_NET_AUTH_URL
    )
    headers = {"Authorization": f"Bearer {battle_net_token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return 0
            
            json_data = await response.json()
            return json_data["price"] / 10000