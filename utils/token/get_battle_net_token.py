import requests


def get_battle_net_token(client_id: str, client_secret: str, base_url: str) -> str:
    data = {"grant_type": "client_credentials"}

    return requests.post(
        base_url,
        auth=(client_id, client_secret),
        data=data,
    ).json()["access_token"]
