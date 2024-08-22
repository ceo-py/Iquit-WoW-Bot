import discord
from .base_modal_add_remove_character import BaseAddRemoveModal


class RemoveCharacterModal(BaseAddRemoveModal):
    TITLE = "Remove Character from Server"

    def __init__(self, *args, **kwargs):
        super().__init__(title=self.TITLE, *args, **kwargs)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        character_region_realm_name_dict = self.create_character_dict(
            self.CHARACTER_MAIN_DETAILS, [self.region, self.realm, self.character_name]
        )

        await interaction.response.send_message(
            "This character already exists in this Discord server.",
            ephemeral=True,
        )
        return

        await interaction.response.defer()
