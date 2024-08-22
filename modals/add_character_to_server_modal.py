import discord
from .base_modal_add_remove_character import BaseAddRemoveModal
from utils.emojis_discord.character_emojis import character_emojis
from database.models.character import Character
from scripts.api.request_character_information import get_wow_character
from database.service.server_service import get_server_by_discord_id, create_server
from database.service.character_server_service import (
    get_character_by_id_with_server_id,
    create_character_server,
)
from database.service.character_service import create_character


class AddCharacterModal(BaseAddRemoveModal):
    TITLE = "Add Character to Server"

    def __init__(self, *args, **kwargs):
        super().__init__(title=self.TITLE, *args, **kwargs)

    async def create_character_in_db(
        self, character: dict, character_main_fields: dict
    ) -> Character:
        return await create_character(
            **self.create_character_dict(
                self.CHARACTER_MAIN_DETAILS + self.CHARACTER_DETAILS,
                [
                    *list(character_main_fields.values()),
                    character.get("class"),
                    0,
                    0,
                    0,
                    0,
                ],
            )
        )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        character = await get_wow_character(self.character_region_realm_name_dict)

        if character.get("statusCode") != 200 and not character.get("name"):
            await interaction.response.send_message(
                "Unable to find the character. Please ensure you've entered the correct information:\n• Region: Check if you've used the correct abbreviation (US, EU, KR, or TW)\n• Realm: Verify the realm name and check for any typos\n• Character Name: Confirm the spelling of your character's name\nIf you're still having issues, try logging into the game to verify your character details.",
                ephemeral=True,
            )
            return

        found_character_in_db = await self.found_character_in_db()

        character_class = (
            character.get("class")
            if not found_character_in_db
            else found_character_in_db.character_class
        )

        character = (
            await self.create_character_in_db(
                character, self.character_region_realm_name_dict
            )
            if not found_character_in_db
            else found_character_in_db
        )

        character_details_for_message = f"{character_emojis.get(character_class)} {self.character_details_for_discord}"
        server = await get_server_by_discord_id(interaction.channel_id)

        if not server:
            server = await create_server(interaction.channel_id)

        character_server = await get_character_by_id_with_server_id(
            character.id, server.id
        )

        if not character_server:
            await create_character_server(character.id, server.id, 0)
        else:
            await interaction.response.send_message(
                f"Character already exists in this server: {character_details_for_message}.",
                ephemeral=True,
            )
            return

        message = f"Character successfully added to the server: {character_details_for_message}."

        try:
            await interaction.response.send_message(message)
        except discord.errors.Forbidden as e:
            print(f"AddCharacterModal:\n{e}")
            await interaction.response.defer()
