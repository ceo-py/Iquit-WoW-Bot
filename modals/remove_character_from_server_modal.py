import discord
from .base_modal_add_remove_character import BaseAddRemoveModal
from database.service.character_server_service import (
    get_character_by_id_with_server_id,
    delete_character_from_server,
)
from database.service.server_service import get_server_by_discord_id
from utils.emojis_discord.character_emojis import character_emojis


class RemoveCharacterModal(BaseAddRemoveModal):
    TITLE = "Remove Character from Server"

    def __init__(self, *args, **kwargs):
        super().__init__(title=self.TITLE, *args, **kwargs)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        found_character_in_db = await self.found_character_in_db()

        if not found_character_in_db:
            await interaction.response.send_message(
                f"Character does not exist in this server: {self.character_details_for_discord}.",
                ephemeral=True,
            )
            return

        server = await get_server_by_discord_id(interaction.channel_id)

        if not server:
            await interaction.response.send_message(
                f"Character does not exist in this server: {self.character_details_for_discord}.",
                ephemeral=True,
            )
            return

        found_character_in_discord_server = await get_character_by_id_with_server_id(
            found_character_in_db.id, server.id
        )

        if found_character_in_discord_server is None:
            await interaction.response.send_message(
                f"Character does not exist in this server: {self.character_details_for_discord}.",
                ephemeral=True,
            )
            return

        await delete_character_from_server(found_character_in_db.id, server.id)
        await interaction.response.send_message(
            f"Character successfully removed from the server: {character_emojis.get(found_character_in_db.character_class)} {self.character_details_for_discord}.",
        )
