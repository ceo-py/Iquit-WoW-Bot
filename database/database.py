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

    def add_character_to_db(
        self,
        region,
        realm,
        character_name,
        player_nickname,
        class_,
        char_class,
        id_channel,
    ):
        self.client["WOW"][f"Channel id {id_channel}"].insert_one(
            {
                f"Region": region.strip(),
                "Realm": realm.strip(),
                "Character Name": character_name.strip(),
                "Player Nickname": player_nickname.strip(),
                "Class": class_.strip(),
                "Class to display": char_class.strip(),
                "Total Rating": 0,
                "DPS": 0,
                "Healer": 0,
                "Tank": 0,
            }
        )

    @staticmethod
    def _change__into_space(data: dict):
        return {k.replace("_", " "): v for k, v in data.items()}

    async def find_character_in_db(self, id_channel: str, **kwargs):
        data = db_._change__into_space(kwargs)
        return self.client["WOW"][f"Channel id {id_channel}"].find_one({"$and": [data]})

    async def update_character_info(
        self,
        id_channel: str,
        character_name: str,
        total: int,
        dps: int,
        heal: int,
        tank: int,
    ) -> None:
        self.client["WOW"][f"Channel id {id_channel}"].update_one(
            {"Character Name": character_name.lower()},
            {"$set": {"Total Rating": total, "DPS": dps, "Healer": heal, "Tank": tank}},
        )

    def save_msg_id(self, server_id, channel_id):
        self.client["WOW"]["Buttons"].insert_one(
            {"Server Id": server_id, "Channel Id": channel_id}
        )

    def reset_season_rating(self):
        for channel in self.client["WOW"].list_collections():
            if "Channel" not in channel["name"]:
                continue
            self.client["WOW"][channel["name"]].update_many(
                {}, {"$set": {"Total Rating": 0, "DPS": 0, "Healer": 0, "Tank": 0}}
            )

    async def delete_user_from_db(self, id_channel: str, character_name: str):
        character_name = character_name.lower()
        players = self.players(id_channel)
        player_found = players.find_one({"Character Name": f"{character_name}"})
        if not player_found:
            return f"**{character_name.capitalize()}** was not found!"

        players.delete_one({"Character Name": f"{character_name}"})
        return f"**{character_name.capitalize()}** was successfully delete from rank data base!"


db_ = DataBaseInfo()
