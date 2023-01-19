import discord
from character_info import CharacterInfo, db_
from modals.add_character import AddCharacterModal
from other_commands import emojis
from sorting_ranks import RankCharacterDisplay


char_info = CharacterInfo()
char_display = RankCharacterDisplay()


class ButtonsCharacterStatistics(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @staticmethod
    async def send_message(
        interaction: discord.Interaction, type_rating: str, role: str
    ) -> None:
        await interaction.response.send_message(
            f"**Loading** {emojis('loading')}",
            ephemeral=True,
        )
        response = await interaction.original_response()
        await response.edit(
            content=f"{emojis('white_arrow_right')} **{type_rating}** {emojis('white_arrow_left')}\n"
            f"```cs\n{await button_info_display(role, str(interaction.channel.id))}```"
        )

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="1",
        emoji=emojis("total"),
    )
    async def total(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ButtonsCharacterStatistics.send_message(interaction, "TOP Total", "Total")

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="2",
        emoji=emojis("dps"),
    )
    async def dps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ButtonsCharacterStatistics.send_message(interaction, "TOP DPS", "DPS")

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="3",
        emoji=emojis("healer"),
    )
    async def heal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ButtonsCharacterStatistics.send_message(
            interaction, "TOP Healers", "Heal"
        )

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.gray,
        custom_id="4",
        emoji=emojis("tank"),
    )
    async def tank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await ButtonsCharacterStatistics.send_message(interaction, "TOP Tanks", "Tank")

    @discord.ui.button(
        label="Add character to server!",
        style=discord.ButtonStyle.red,
        custom_id="5",
        emoji=emojis("player_add"),
    )
    async def add_character(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(AddCharacterModal())


async def button_info_display(type_of_info, channel_id, backup=None):
    data_db = await char_info.get_data_for_rank(channel_id, backup)
    data_db = char_display.sorting_db(data_db, f"{type_of_info}")
    return char_display.button_rank_result(data_db, f"{type_of_info}")
