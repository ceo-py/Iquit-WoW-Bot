import discord
from .base_modal_add_remove_character import BaseAddRemoveModal
from database.models.character import Character
from scripts.api.request_character_information import get_wow_character
from database.service.server_service import get_server_by_discord_id, create_server
from database.service.character_server_service import (
    get_character_server_by_id,
    create_character_server,
)
from database.service.character_service import (
    get_character_by_region_realm_name,
    create_character,
)


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
        character_region_realm_name_dict = self.create_character_dict(
            self.CHARACTER_MAIN_DETAILS, [self.region, self.realm, self.character_name]
        )

        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.", ephemeral=True
            )
            return

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

        character = (
            await self.create_character_in_db(
                character, character_region_realm_name_dict
            )
            if not found_character_in_db
            else found_character_in_db
        )

        current_channel = self.find_discord_channel(guild.text_channels)
        server = await get_server_by_discord_id(current_channel.id)

        if not server:
            server = await create_server(current_channel.id)

        character_server = await get_character_server_by_id(character.id)

        if not character_server:
            await create_character_server(character.id, server.id, 0)
        else:
            await interaction.response.send_message(
                "This character already exists in this Discord server.",
                ephemeral=True,
            )
            return

        message = f"Character successfully added to the server: **{str(self.character_name).capitalize()}** from **{str(self.realm).capitalize()}** - **{str(self.region).capitalize()}**."

        try:
            await current_channel.send(message)
        except discord.errors.Forbidden as e:
            print(f"AddCharacterModal:\n{e}")

        await interaction.response.defer()
