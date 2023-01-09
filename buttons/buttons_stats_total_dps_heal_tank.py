import discord
from character_info import CharacterInfo, db_
from modals.add_character import AddCharacterModal
from sorting_ranks import RankCharacterDisplay

char_info = CharacterInfo()
char_display = RankCharacterDisplay()


class ButtonsCharacterStatistics(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="1",
        emoji="<:Totalrole:1058488589459136512>",
    )
    async def total(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message(
            f"```TOP Total\n{await button_info_display('Total', str(button.channel.id))}```",
            ephemeral=True,
        )

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="2",
        emoji="<:DPSrole:1058479594438668468>",
    )
    async def dps(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message(
            f"```TOP DPS\n{await button_info_display('DPS', str(button.channel.id))}```",
            ephemeral=True,
        )

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="3",
        emoji="<:Healerrole:1058479567616090222>",
    )
    async def heal(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message(
            f"```TOP Healers\n{await button_info_display('Heal', str(button.channel.id))}```",
            ephemeral=True,
        )

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="4",
        emoji="<:Tankrole:1058479529158529124>",
    )
    async def tank(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message(
            f"```TOP Tanks\n{await button_info_display('Tank', str(button.channel.id))}```",
            ephemeral=True,
        )

    @discord.ui.button(
        label="Add character to server!", style=discord.ButtonStyle.red, custom_id="5"
    )
    async def add_character(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await button.response.send_modal(AddCharacterModal())


async def button_info_display(type_of_info, channel_id, backup=None):
    data_db = await char_info.get_data_for_rank(channel_id, backup)
    data_db = char_display.sorting_db(data_db, f"{type_of_info}")
    return char_display.button_rank_result(data_db, f"{type_of_info}")
