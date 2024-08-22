import discord
from .base_modal_add_remove_character import BaseAddRemoveModal


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

        await interaction.response.send_message(
            f"Character successfully removed from the server: {self.character_details_for_discord}.",
        )
        return

        await interaction.response.defer()
