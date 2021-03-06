class RankCharacterDisplay:
    @staticmethod
    def sorting_db(data_characters, how_to_sort):
        data_characters = sorted(data_characters, key=lambda x: -x[f"{how_to_sort}"])
        return data_characters

    @staticmethod
    def get_all_chars(data_info):
        all_ranks = {pos: f"{pos}. n/a" for pos in range(1, 10)}
        for pos, show in enumerate(data_info, 1):
            if pos > 9 or show['Total'] == 0:
                break
            all_ranks[pos] = f"[{pos}.{show['Character Name']}:{show['Total']}]({show['Player Armory']})"
        return all_ranks

    @staticmethod
    def get_other_ranks(data_info, what_rank):
        result_ = {pos: "n/a" for pos in range(1, 4)}
        for pos, show in enumerate(data_info, 1):
            if pos > 3 or show[f'{what_rank}'] == 0:
                break
            result_[pos] = f"[{show['Character Name']}:{show[f'{what_rank}']}]({show['Player Armory']})"
        return result_

    @staticmethod
    def button_rank_result(data_info, what_rank):
        show_list_result = ""
        for pos, show in enumerate(data_info, 1):
            if show[f'{what_rank}'] == 0:
                break
            show_list_result += f"{pos}.{show['Character Name']}: {show[f'{what_rank}']}\n"
        if show_list_result:
            return show_list_result
        return "There are no characters with greater than 0 rating!"
