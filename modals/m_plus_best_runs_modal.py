import discord
from .base_modal_add_remove_character import BaseAddRemoveModal
from scripts.api.request_character_information import get_wow_character_check


class MPlusBestRunsModal(BaseAddRemoveModal):
    TITLE = "Show top Mythic+ runs across all dungeons."

    def __init__(self, *args, **kwargs):
        super().__init__(title=self.TITLE, *args, **kwargs)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        character = await get_wow_character_check(self.character_region_realm_name_dict)

        if character.get("statusCode") != 200 and not character.get("name"):
            await self.send_character_not_exist_message_in_battle_net(interaction)
            return

        dungeon_runs = character.get("mythic_plus_best_runs", [])

        if not dungeon_runs:
            await interaction.response.send_message(
                f"The character {interaction.client.character_emojis.get(character['class'].lower())} **{character['name']}** hasn't completed any Mythic+ dungeons yet.",
            )
