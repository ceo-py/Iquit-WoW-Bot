import discord
from .base_modal_add_remove_character import BaseAddRemoveModal
from utils.emojis_discord.character_emojis import character_emojis
from scripts.api.request_character_information import get_wow_character


class CheckCharacterModal(BaseAddRemoveModal):
    TITLE = "Check Character Progression"

    def __init__(self, *args, **kwargs):
        super().__init__(title=self.TITLE, *args, **kwargs)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        character = await get_wow_character(self.character_region_realm_name_dict)

        if character.get("statusCode") != 200 and not character.get("name"):
            await self.send_character_not_exist_message_in_battle_net(interaction)
            return
        print(character)
        message = f"OMG im just gonna shake it !!!"

        await interaction.response.send_message(message)
