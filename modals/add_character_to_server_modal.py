import discord
from settings import DISCORD_CHANNEL_NAME
from scripts.api.request_character_information import get_wow_character
from utils.convert_dict_k_v_into_small_letters import convert_dict_k_v_small_letters
from database.service.server_service import get_server_by_discord_id, create_server
from database.service.character_service import (
    get_character_by_region_realm_name,
    create_character,
)


class AddCharacterModal(discord.ui.Modal, title="Add Character to Server"):
    CHARACTER_MAIN_DETAILS = ["region", "realm", "name"]
    CHARACTER_DETAILS = [
        "character_class",
        "total_rating",
        "dps_rating",
        "healer_rating",
        "tank_rating",
    ]

    region = discord.ui.TextInput(
        label="Server Region",
        placeholder="Enter the server region (e.g., US, EU, KR, TW)",
        max_length=2,
    )
    realm = discord.ui.TextInput(
        label="Character Realm",
        placeholder="Enter your character's realm (e.g., Kazzak, Draenor)",
        max_length=26,
    )
    character_name = discord.ui.TextInput(
        label="Character Name",
        placeholder="Enter your in-game character name",
        max_length=12,
    )

    @staticmethod
    def find_discord_channel(channels: "interaction.guild") -> int:
        for channel in channels:
            if channel.name == DISCORD_CHANNEL_NAME:
                return channel

    @staticmethod
    def create_character_dict(keys_: list, values_: list) -> dict:
        return convert_dict_k_v_small_letters(dict(zip(keys_, values_)))

    async def create_character_in_db(
        self, character: dict, character_main_fields: dict
    ) -> None:
        return await create_character(
            **self.create_character_dict(
                self.CHARACTER_MAIN_DETAILS + self.CHARACTER_DETAILS,
                [
                    *list(character_main_fields.values()),
                    character.get("class"),
                    character.get("mythic_plus_scores_by_season", [""])[0]
                    .get("scores", {})
                    .get("all", 0),
                    character.get("mythic_plus_scores_by_season", [""])[0]
                    .get("scores", {})
                    .get("dps", 0),
                    character.get("mythic_plus_scores_by_season", [""])[0]
                    .get("scores", {})
                    .get("healer", 0),
                    character.get("mythic_plus_scores_by_season", [""])[0]
                    .get("scores", {})
                    .get("tank", 0),
                ],
            )
        )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        character_region_realm_name_dict = self.create_character_dict(
            self.CHARACTER_MAIN_DETAILS, [self.region, self.realm, self.character_name]
        )

        character = await get_wow_character(character_region_realm_name_dict)

        if character.get("statusCode") != 200 and not character.get("name"):
            await interaction.response.send_message(
                "Unable to find the character. Please ensure you've entered the correct information:\n• Region: Check if you've used the correct abbreviation (US, EU, KR, or TW)\n• Realm: Verify the realm name and check for any typos\n• Character Name: Confirm the spelling of your character's name\nIf you're still having issues, try logging into the game to verify your character details.",
                ephemeral=True,
            )
            return
        found_character_in_db = await get_character_by_region_realm_name(
            **character_region_realm_name_dict
        )

        if not found_character_in_db:
            await self.create_character_in_db(
                character, character_region_realm_name_dict
            )

        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.", ephemeral=True
            )
            return

        current_channel = self.find_discord_channel(guild.text_channels)
        server = await get_server_by_discord_id(current_channel.id)

        if not server:
            server = await create_server(current_channel.id)
        message = f"Character successfully added to the server: **{str(self.character_name).capitalize()}** from **{str(self.realm).capitalize()}** - **{str(self.region).capitalize()}**."

        try:
            await current_channel.send(message)
        except discord.errors.Forbidden as e:
            print(f"AddCharacterModal:\n{e}")

        await interaction.response.defer()
