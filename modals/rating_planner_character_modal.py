import discord
from .base_modal_add_remove_character import BaseAddRemoveModal
from database.models.character import Character
from utils.api.request_character_information import get_wow_character
from database.service.server_service import get_server_by_discord_id, create_server
from database.service.character_server_service import (
    get_character_by_id_with_server_id,
    create_character_server,
)
from database.service.character_service import create_character
from database.service.dungeon_run_service import update_or_create_dungeon_run
from database.service.dungeon_service import get_all_dungeons


class RatingPlannerModal(BaseAddRemoveModal):
    TITLE = "Rating Planner"

    def __init__(self, *args, **kwargs):
        super().__init__(title=self.TITLE, *args, **kwargs)

        self.max_key_level = discord.ui.TextInput(
            label="Max Key Level",
            placeholder="Dungeon key level (2-20)",
            max_length=12,
        )

        self.add_item(self.max_key_level)

    async def on_submit(self, interaction: discord.Interaction) -> None:

        await interaction.response.defer()

        # character_fetch_data = await get_wow_character(
        #     self.character_region_realm_name_dict
        # )

        # character_details_for_message = f"{interaction.client.character_emojis.get(character_class.lower())} {self.character_details_for_discord(interaction)}"
        # server = await get_server_by_discord_id(interaction.channel_id)

        # try:
        #     await interaction.followup.send(message)
        # except discord.errors.Forbidden as e:
        #     print(f"AddCharacterModal:\n{e}")
