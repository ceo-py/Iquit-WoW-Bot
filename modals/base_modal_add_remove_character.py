import discord
from abc import ABC, abstractmethod
from utils.convert_dict_k_v_into_small_letters import convert_dict_k_v_small_letters
from database.service.character_service import get_character_by_region_realm_name
from database.models.character import Character


class BaseAddRemoveModal(ABC, discord.ui.Modal):
    CHARACTER_MAIN_DETAILS = ["region", "realm", "name"]
    CHARACTER_DETAILS = [
        "character_class",
        "total_rating",
        "dps_rating",
        "healer_rating",
        "tank_rating",
    ]

    def __init__(self, title="", *args, **kwargs):
        super().__init__(title=title, *args, **kwargs)

        self.region = discord.ui.TextInput(
            label="Server Region",
            placeholder="Enter the server region (e.g., US, EU, KR, TW)",
            max_length=2,
        )
        self.realm = discord.ui.TextInput(
            label="Character Realm",
            placeholder="Enter your character's realm (e.g., Kazzak, Draenor)",
            max_length=26,
        )
        self.character_name = discord.ui.TextInput(
            label="Character Name",
            placeholder="Enter your in-game character name",
            max_length=12,
        )

        self.add_item(self.region)
        self.add_item(self.realm)
        self.add_item(self.character_name)

    @staticmethod
    def create_character_dict(keys_: list, values_: list) -> dict:
        return convert_dict_k_v_small_letters(dict(zip(keys_, values_)))

    @property
    def character_details_for_discord(self):
        return f"**{str(self.character_name).capitalize()}** from **{str(self.realm).capitalize()}** - **{str(self.region).capitalize()}**."

    @property
    def character_region_realm_name_dict(self) -> dict:
        return self.create_character_dict(
            self.CHARACTER_MAIN_DETAILS, [
                self.region, self.realm, self.character_name]
        )

    async def found_character_in_db(self) -> Character:
        return await get_character_by_region_realm_name(
            **self.character_region_realm_name_dict
        )

    @abstractmethod
    async def on_submit(self, interaction: discord.Interaction) -> None:
        pass
