import discord
from .base_modal_add_remove_character import BaseAddRemoveModal
from database.service.character_server_service import (
    get_character_by_id_with_server_id,
    delete_character_from_server,
)
from database.service.server_service import get_server_by_discord_id
from database.service.character_server_service import get_character_by_id
from database.service.character_service import delete_character
from database.service.dungeon_run_service import delete_dungeon_run


class RemoveCharacterModal(BaseAddRemoveModal):
    TITLE = "Remove Character from Server"

    def __init__(self, *args, **kwargs):
        super().__init__(title=self.TITLE, *args, **kwargs)

    async def send_character_not_exist_message_in_db(
        self, interaction: discord.Interaction
    ):
        await interaction.followup.send(
            f"Character does not exist in this server: {self.character_details_for_discord(interaction)}.",
            ephemeral=True,
        )

    async def send_success_message(self, interaction: discord.Interaction, character):
        await interaction.followup.send(
            f"Character successfully removed from the server: {interaction.client.character_emojis.get(character.character_class)} {self.character_details_for_discord(interaction)}.",
        )

    async def delete_character_from_db_if_no_discord_server(self, character_id):

        character_in_another_discord_server = await get_character_by_id(character_id)
        if character_in_another_discord_server is None:
            await delete_character(character_id)
            await delete_dungeon_run(character_id)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        found_character_in_db = await self.found_character_in_db()

        if not found_character_in_db:
            await self.send_character_not_exist_message_in_db(interaction)
            return

        server = await get_server_by_discord_id(interaction.channel_id)

        found_character_in_discord_server = await get_character_by_id_with_server_id(
            found_character_in_db.id, server.id
        )

        if found_character_in_discord_server is None:
            await self.send_character_not_exist_message_in_db(interaction)
            await self.delete_character_from_db_if_no_discord_server(
                found_character_in_db.id
            )
            return

        if not server:
            await self.send_character_not_exist_message_in_db(interaction)
            return

        await delete_character_from_server(found_character_in_db.id, server.id)
        await self.send_success_message(interaction, found_character_in_db)
        await self.delete_character_from_db_if_no_discord_server(
            found_character_in_db.id
        )
