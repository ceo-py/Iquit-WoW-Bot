import discord
from utils.emojis import get_emojis
from modals.add_character_to_server_modal import AddCharacterModal


class ButtonsCharacterStatistics(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

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
            f"```test```"
        )

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="1",
        emoji="<:Totalrole:1058488589459136512>",
    )
    async def total(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ButtonsCharacterStatistics.send_message(interaction, "TOP Total", "total")

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="2",
        emoji="<:DPSrole:1058479594438668468>",
    )
    async def dps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ButtonsCharacterStatistics.send_message(interaction, "TOP DPS", "dps")

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="3",
        emoji="<:Healerrole:1058479567616090222>",
    )
    async def heal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ButtonsCharacterStatistics.send_message(interaction, "TOP Heal", "total")

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="4",
        emoji="<:Tankrole:1058479529158529124>",
    )
    async def tank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ButtonsCharacterStatistics.send_message(interaction, "TOP Tank", "total")

    @discord.ui.button(
        label="Add Character to Server",
        style=discord.ButtonStyle.red,
        custom_id="5",
        emoji="<:6332logmemberplusw:1065621500855586907>",
    )
    async def add_character_to_server(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(AddCharacterModal())
