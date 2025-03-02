import discord
from modals.add_character_to_server_modal import AddCharacterModal
from database.service.server_service import get_server_by_discord_id
from database.service.character_server_service import (
    get_all_characters_from_discord_server_by_id,
)
from database.service.character_service import get_characters_by_ids
from utils.character.character_ranking import filter_and_sort_characters_by_role
from settings import (
    MESSAGE_CHARACTER_LIMIT,
    CHARACTER_ROLES,
    TOTAL_EMOJI,
    DPS_EMOJI,
    HEAL_EMOJI,
    TANK_EMOJI,
    ADD_EMOJI,
)


class ButtonsCharacterStatistics(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @staticmethod
    async def generate_message(interaction: discord.Interaction, role: str) -> str:

        discord_server_instance = await get_server_by_discord_id(interaction.guild_id)

        if not discord_server_instance:
            return '''There aren't any characters added yet. To add characters and view rankings, type /add.'''

        all_characters_in_discord_server_ids = (
            await get_all_characters_from_discord_server_by_id(
                discord_server_instance.id
            )
        )
        all_characters = filter_and_sort_characters_by_role(
            await get_characters_by_ids(
                [
                    character.character_id
                    for character in all_characters_in_discord_server_ids
                ]
            ),
            role,
        )

        output = ""

        for pos, character in enumerate(all_characters, 1):
            character_message = f"{pos}.{character.name.capitalize()}: {int(getattr(character, CHARACTER_ROLES.get(role, 'total_rating')))}\n"

            if len(output) + len(character_message) > MESSAGE_CHARACTER_LIMIT:
                break

            output += character_message

        return (
            output
            if output
            else f"No characters found with a rating above 0 for {role} role"
        )

    @staticmethod
    async def send_message(
        interaction: discord.Interaction, type_rating: str, role: str
    ) -> None:
        await interaction.response.send_message(
            f"**Loading** {interaction.client.common_emojis.get('loading')}",
            ephemeral=True,
        )
        response = await interaction.original_response()
        await response.edit(
            content=f"{interaction.client.common_emojis.get('white_arrow_right')} **{type_rating}**"
            f" {interaction.client.common_emojis.get('white_arrow_left')}\n"
            f"```cs\n{await ButtonsCharacterStatistics.generate_message(interaction, role)}```"
        )

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="1",
        emoji=TOTAL_EMOJI,
    )
    async def total(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ButtonsCharacterStatistics.send_message(interaction, "TOP Total", "total")

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="2",
        emoji=DPS_EMOJI,
    )
    async def dps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ButtonsCharacterStatistics.send_message(interaction, "TOP DPS", "dps")

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="3",
        emoji=HEAL_EMOJI,
    )
    async def heal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ButtonsCharacterStatistics.send_message(interaction, "TOP Heal", "heal")

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="4",
        emoji=TANK_EMOJI,
    )
    async def tank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ButtonsCharacterStatistics.send_message(interaction, "TOP Tank", "tank")

    @discord.ui.button(
        label="Add Character to Server",
        style=discord.ButtonStyle.green,
        custom_id="5",
        emoji=ADD_EMOJI,
    )
    async def add_character_to_server(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(AddCharacterModal())
