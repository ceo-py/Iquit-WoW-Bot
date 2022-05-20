import os
import pymongo
from urllib.parse import quote_plus
from dotenv import load_dotenv


class DataBaseInfo:
    def __init__(self):
        self.db_info = None

    def connect_db(self, id_channel, msg_check=False):
        load_dotenv()
        self.db_info = None
        username = quote_plus(os.getenv("DB_USER_NAME"))
        password = quote_plus(os.getenv("DB_PASSWORD"))
        uri = f"mongodb+srv://{username}:{password}@maindata.sqlqx.mongodb.net/myFirstDatabase?retryWrites=true&w" \
              f"=majority "
        client = pymongo.MongoClient(uri)
        if msg_check:
            self.db_info = client["WOW"]["Buttons"]
            return self.db_info
        self.db_info = client["WOW"][f"Channel id {id_channel}"]
        return self.db_info

    def add_character_to_db(self, info):
        region, realm, character_name, player_nickname, class_ = info.split()
        self.db_info.insert_one({f"Region": region, "Realm": realm, "Character Name": character_name,
                                 "Player Nickname": player_nickname, "Class": class_, "Total Rating": 0,
                                 "DPS": 0, "Healer": 0, "Tank": 0})

    def save_msg_id(self, server_id, channel_id):
        self.db_info.insert_one({"Server Id": server_id, "Channel Id": channel_id})


db_ = DataBaseInfo()
