import discord
from character_info import CharacterInfo
from sorting_ranks import RankCharacterDisplay

char_info = CharacterInfo()
char_display = RankCharacterDisplay()


class ButtonsCharacterStatistics(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=" - Total Rank!", style=discord.ButtonStyle.gray, custom_id="1", emoji="\U0001F4C8")
    async def total(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message(
            f"```TOP Total\n{await button_info_display('Total', str(button.channel.id))}```", ephemeral=True)

    @discord.ui.button(label=" - Ranks!", style=discord.ButtonStyle.gray, custom_id="2", emoji="\U00002694")
    async def dps(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message(
            f"```TOP DPS\n{await button_info_display('DPS', str(button.channel.id))}```", ephemeral=True)

    @discord.ui.button(label=" - Ranks!", style=discord.ButtonStyle.gray, custom_id="3", emoji="\U00002764")
    async def heal(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message(
            f"```TOP Healers\n{await button_info_display('Heal', str(button.channel.id))}```", ephemeral=True)

    @discord.ui.button(label=" - Ranks!", style=discord.ButtonStyle.gray, custom_id="4", emoji="\U0001F6E1")
    async def tank(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_message(
            f"```TOP Tanks\n{await button_info_display('Tank', str(button.channel.id))}```", ephemeral=True)


async def button_info_display(type_of_info, channel_id, backup=None):
    data_db = await char_info.get_data_for_rank(channel_id, backup)
    data_db = char_display.sorting_db(data_db, f"{type_of_info}")
    return char_display.button_rank_result(data_db, f"{type_of_info}")