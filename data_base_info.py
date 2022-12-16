import os
import pymongo
from urllib.parse import quote_plus
from dotenv import load_dotenv


load_dotenv()


class DataBaseInfo:
    __DB_SINGLETON = []

    def __init__(self):
        if not DataBaseInfo.__DB_SINGLETON:
            username = quote_plus(os.getenv("DB_USER_NAME"))
            password = quote_plus(os.getenv("DB_PASSWORD"))
            uri = f"mongodb+srv://{username}:{password}@cluster0.1sxtc.mongodb.net/?retryWrites=true&w=majority"
            DataBaseInfo.__DB_SINGLETON.append(pymongo.MongoClient(uri))

        self.client = DataBaseInfo.__DB_SINGLETON[0]

    def connect_db(self, id_channel, msg_check=False):
        if msg_check:
            return self.client["WOW"]["Buttons"]

        return self.client["WOW"][f"Channel id {id_channel}"]

    def add_character_to_db(self, *info):
        region, realm, character_name, player_nickname, class_, id_channel = info
        self.client["WOW"][f"Channel id {id_channel}"].insert_one({f"Region": region, "Realm": realm, "Character Name": character_name,
                                 "Player Nickname": player_nickname, "Class": class_, "Total Rating": 0,
                                 "DPS": 0, "Healer": 0, "Tank": 0})

    def save_msg_id(self, server_id, channel_id):
        self.client["WOW"]["Buttons"].insert_one({"Server Id": server_id, "Channel Id": channel_id})

