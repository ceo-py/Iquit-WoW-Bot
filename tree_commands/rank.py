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
