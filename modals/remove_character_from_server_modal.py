import discord
from modals.base_character_modal import BaseCharacterModal
from database.models.character_server import CharacterServer
from database.service.character_server_service import (
    get_character_by_id_with_server_id,
)
from database.service.server_service import get_server_by_discord_id
from database.service.character_server_service import get_character_by_id
from database.service.character_service import delete_character
from database.service.dungeon_run_service import delete_dungeon_run
from utils.character.server_ranking_recompute import recompute_server_rankings
from tortoise.transactions import in_transaction


class RemoveCharacterModal(BaseCharacterModal):
    TITLE = "Remove character: paste URL or type details"

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
            f"Character successfully removed from the server: {interaction.client.character_emojis.get(character.character_class, '')} {self.character_details_for_discord(interaction)}.",
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

        server = await get_server_by_discord_id(interaction.guild_id)

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

        # Transaction: delete link and recompute ranks atomically (per-server lock)
        try:
            async with in_transaction() as tx:
                await tx.execute_query("SELECT pg_advisory_xact_lock($1);", [server.id])
                await CharacterServer.using_db(tx).filter(
                    character_id=found_character_in_db.id, server_id=server.id
                ).delete()
                await recompute_server_rankings(server.id, conn=tx)
        except Exception:
            await interaction.followup.send(
                "Failed to remove character due to a database error.", ephemeral=True
            )
            raise

        await self.send_success_message(interaction, found_character_in_db)
        await self.delete_character_from_db_if_no_discord_server(
            found_character_in_db.id
        )
