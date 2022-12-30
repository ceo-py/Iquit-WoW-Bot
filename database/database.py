import os
import pymongo
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


def db_connection():
    username = quote_plus(os.getenv("DB_USER_NAME"))
    password = quote_plus(os.getenv("DB_PASSWORD"))
    uri = f"mongodb+srv://{username}:{password}@cluster0.1sxtc.mongodb.net/?retryWrites=true&w=majority"
    return pymongo.MongoClient(uri)


class Singleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


class DataBaseInfo(Singleton):

    def __init__(self):
        self.client = db_connection()

    def connect_db(self, id_channel, msg_check=False):
        if msg_check:
            return self.client["WOW"]["Buttons"]

        return self.client["WOW"][f"Channel id {id_channel}"]

    def players(self, id_channel):
        return self.client["WOW"][f"Channel id {id_channel}"]

    def buttons(self):
        return self.client["WOW"]["Buttons"]

    def add_character_to_db(self, region, realm, character_name, player_nickname, class_, id_channel):
        self.client["WOW"][f"Channel id {id_channel}"].insert_one(
            {f"Region": region, "Realm": realm, "Character Name": character_name,
             "Player Nickname": player_nickname, "Class": class_, "Total Rating": 0,
             "DPS": 0, "Healer": 0, "Tank": 0})

    @staticmethod
    def _change__into_space(data: dict):
        return {k.replace("_", " "): v for k, v in data.items()}

    async def find_character_in_db(self, id_channel: str, **kwargs):
        data = db_._change__into_space(kwargs)
        return self.client["WOW"][f"Channel id {id_channel}"].find_one({"$and": [data]})

    async def update_character_info(self, id_channel: str, character_name: str, total: int, dps: int, heal: int,
                              tank: int) -> None:
        self.client["WOW"][f"Channel id {id_channel}"].update_one({"Character Name": character_name.lower()}, {"$set":{
            "Total Rating": total, "DPS": dps, "Healer": heal, "Tank": tank
        }})

    def save_msg_id(self, server_id, channel_id):
        self.client["WOW"]["Buttons"].insert_one({"Server Id": server_id, "Channel Id": channel_id})


db_ = DataBaseInfo()
