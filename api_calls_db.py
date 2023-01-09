import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class APICALLDB:
    def __init__(self):
        self.api_url = (
            "https://data.mongodb-api.com/app/data-ussei/endpoint/data/beta/action/find"
        )
        self.headers = {
            "Content-Type": "application/json",
            "Access-Control-Request-Headers": "*",
            "api-key": os.getenv("DB_API"),
        }
        self.payload = None

    def api_call_channels(self, channel_id):
        self.payload = json.dumps(
            {
                "collection": "Buttons",
                "database": "WOW",
                "dataSource": "MainData",
                "filter": {"Channel Id": f"{channel_id}"},
            }
        )
        return requests.request(
            "POST", self.api_url, headers=self.headers, data=self.payload
        ).json()["documents"]

    def api_call_characters(self, channel_id):
        self.payload = json.dumps(
            {
                "collection": f"Channel id {channel_id}",
                "database": "WOW",
                "dataSource": "MainData",
                "filter": {},
            }
        )
        return requests.request(
            "POST", self.api_url, headers=self.headers, data=self.payload
        ).json()["documents"]

    def search_for_character_in_api(self, channel_id, c_region, c_realm, c_name):
        self.payload = json.dumps(
            {
                "collection": f"Channel id {channel_id}",
                "database": "WOW",
                "dataSource": "MainData",
                "filter": {
                    f"Region": c_region,
                    "Realm": c_realm,
                    "Character Name": c_name,
                },
            }
        )
        return requests.request(
            "POST", self.api_url, headers=self.headers, data=self.payload
        ).json()["documents"]
