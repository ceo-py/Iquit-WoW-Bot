class RankCharacterDispley:

    def sorting_db(self, data_characters, how_to_sort):
        self.data_characters = []
        self.data_characters = sorted(data_characters, key=lambda x: -x[f"{how_to_sort}"])
        return self.data_characters

    def get_all_chars(self, data_info):
        self.all_ranks = {1: "1. n/a", 2: "2. n/a", 3: "3. n/a", 4: "4. n/a", 5: "5. n/a", 6: "6. n/a",
                          7: "7. n/a", 8: "8. n/a", 9: "9. n/a"}
        for pos, show in enumerate(data_info, 1):
            if pos > 9 or show['Total'] == 0:
                break
            self.all_ranks[pos] = f"[{pos}.{show['Character Name']}:{show['Total']}]({show['Player Armory']})"
        return self.all_ranks

    def get_other_ranks(self, data_info, what_rank):
        result_ = {1: "n/a", 2: "n/a", 3: "n/a"}
        for pos, show in enumerate(data_info, 1):
            if pos > 3 or show[f'{what_rank}'] == 0:
                break
            result_[pos] = f"[{show['Character Name']}:{show[f'{what_rank}']}]({show['Player Armory']})"
        return result_

    def button_rank_result(self, data_info, what_rank):
        show_result = "There are no characters with greater than 0 rating"
        show_list_result = ""
        for pos, show in enumerate(data_info, 1):
            if show[f'{what_rank}'] == 0:
                break
            show_list_result += f"{pos}.{show['Character Name']}: {show[f'{what_rank}']}\n"
        if show_list_result:
            return show_list_result
        return show_result
