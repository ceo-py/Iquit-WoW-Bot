import aiohttp


async def get_battle_net_token(client_id: str, client_secret: str, base_url: str) -> str:
    data = {"grant_type": "client_credentials"}
    auth = aiohttp.BasicAuth(client_id, client_secret)

    async with aiohttp.ClientSession() as session:
        async with session.post(base_url, auth=auth, data=data) as response:
            result = await response.json()
            return result["access_token"]