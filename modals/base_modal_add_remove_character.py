import discord
from abc import ABC, abstractmethod
from settings import DISCORD_CHANNEL_NAME
from utils.convert_dict_k_v_into_small_letters import convert_dict_k_v_small_letters


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
    def find_discord_channel(channels: "interaction.guild") -> int:
        for channel in channels:
            if channel.name == DISCORD_CHANNEL_NAME:
                return channel

    @staticmethod
    def create_character_dict(keys_: list, values_: list) -> dict:
        return convert_dict_k_v_small_letters(dict(zip(keys_, values_)))

    @abstractmethod
    async def on_submit(self, interaction: discord.Interaction) -> None:
        pass
