from typing import Literal

from buttons.buttons_stats_total_dps_heal_tank import char_display
from modals.add_character import char_info
from sorting_ranks import RankCharacterDisplay


class TreeCommands:

    @staticmethod
    async def get_players(interaction, channel_to_find, role_sort):
        role_sort = 'Total' if role_sort == 'All' else role_sort
        for channel in interaction.guild.channels:
            if channel.name == channel_to_find:
                data_db = await char_info.get_data_for_rank(channel.id, None)
                sorted_data = char_display.sorting_db(data_db, role_sort)
                return sorted_data, role_sort

    @staticmethod
    def generate_output(sorted_data, role, top):
        return RankCharacterDisplay.button_rank_result(sorted_data, role, top)

    @staticmethod
    async def message_respond_interaction(interaction, top, role, output):
        await interaction.response.send_message(f'Top {top} {role} \n'
                                                f'>>> ```cs\n{output}```')

    @staticmethod
    async def message_respond_ctx(ctx, top, role, output):
        await ctx.send(f'Top {top} {role} \n>>> ```cs\n{output}```')

    @staticmethod
    def roles():
        return Literal['All', 'DPS', 'Heal', 'Tank']

    @staticmethod
    def top():
        return Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
