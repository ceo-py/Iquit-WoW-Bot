import discord
from abc import ABC, abstractmethod
from utils.convert_dict_k_v_into_small_letters import convert_dict_k_v_small_letters
from database.service.character_service import get_character_by_region_realm_name
from database.models.character import Character


class BaseCharacterModal(ABC, discord.ui.Modal):
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

        self.raider_io_url = discord.ui.TextInput(
            label="Raider.io URL (optional)",
            placeholder="Paste your Raider.io profile URL, or fill in the fields below",
            max_length=120,
            required=False,
        )

        self.region = discord.ui.TextInput(
            label="Server Region (manual entry)",
            placeholder="e.g., US, EU, KR, TW (if not using URL)",
            max_length=2,
            required=False,
        )
        self.realm = discord.ui.TextInput(
            label="Character Realm (manual entry)",
            placeholder="e.g., Kazzak, Draenor (if not using URL)",
            max_length=26,
            required=False,
        )
        self.character_name = discord.ui.TextInput(
            label="Character Name (manual entry)",
            placeholder="Enter your in-game character name (if not using URL)",
            max_length=12,
            required=False,
        )

        self.add_item(self.raider_io_url)
        self.add_item(self.region)
        self.add_item(self.realm)
        self.add_item(self.character_name)

    @staticmethod
    def create_character_dict(keys_: list, values_: list) -> dict:
        return convert_dict_k_v_small_letters(dict(zip(keys_, values_)))

    def character_details_for_discord(self, interaction: discord.Interaction):
        return f"**{str(self.character_name).capitalize()}** from **{str(self.realm).capitalize()}** {interaction.client.region_emojis.get(str(self.region).lower(), '')}"

    @property
    def character_region_realm_name_dict(self) -> dict:
        raider_io_url = [
            x.lower().strip() for x in self.raider_io_url.value.split("/")[-3:]
        ]
        if all(x != "" for x in raider_io_url) and len(raider_io_url) == 3:
            self.region, self.realm, self.character_name = raider_io_url
        return self.create_character_dict(
            self.CHARACTER_MAIN_DETAILS, [self.region, self.realm, self.character_name]
        )

    async def found_character_in_db(self) -> Character:
        return await get_character_by_region_realm_name(
            **self.character_region_realm_name_dict
        )

    async def send_character_not_exist_message_in_battle_net(
        self, interaction: discord.Interaction
    ) -> None:
        await interaction.followup.send(
            "Unable to find the character. Please ensure you've entered the correct information:\n"
            f"• Region: Check if you've used the correct abbreviation (US, EU, KR, or TW)\n"
            f"• Realm: Verify the realm name and check for any typos\n"
            f"• Character Name: Confirm the spelling of your character's name\n"
            f"• Or simply copy and paste your Raider.io character profile URL.\n"
            f"If you're still having issues, try logging into the game to verify your character details.",
            ephemeral=True,
        )

    @abstractmethod
    async def on_submit(self, interaction: discord.Interaction) -> None:
        pass
