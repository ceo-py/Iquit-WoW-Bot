import aiohttp
import asyncio
import requests
from data_base_info import DataBaseInfo

db_ = DataBaseInfo()


class CharacterInfo:
    def __init__(self):
        self.raider_io_info = []

    def get_data_from_rio(self, channel_id, session):
        self.raider_io_info = []
        data_base = db_.connect_db(channel_id)
        for show in data_base.find({}):
            region, realm, name = show["Region"], show["Realm"], show["Character Name"]
            self.raider_io_info.append(session.get(f'https://raider.io/api/v1/characters/profile?region={region}&realm'
                                                   f'={realm}&name={name}&fields=mythic_plus_recent_runs,covenant,gear,'
                                                   f'raid_progression,mythic_plus_scores_by_season%3Aseason-sl-3',
                                                   ssl=False))
        return self.raider_io_info

    async def get_data_for_rank(self, channel_id):
        results = []
        show = []
        async with aiohttp.ClientSession() as session:
            x = ci.get_data_from_rio(channel_id, session)
            responses = await asyncio.gather(*x)
            for response in responses:
                results.append(await response.json())
        for index in results:
            name = index["name"]
            rating = int(format(index['mythic_plus_scores_by_season'][0]["segments"]["all"]["score"], ".0f"))
            tank_r = int(format(index['mythic_plus_scores_by_season'][0]["segments"]["tank"]["score"], ".0f"))
            dps_r = int(format(index['mythic_plus_scores_by_season'][0]["segments"]["dps"]["score"], ".0f"))
            heal_r = int(format(index['mythic_plus_scores_by_season'][0]["segments"]["healer"]["score"], ".0f"))
            player_url = index["profile_url"]
            if rating != 0:
                show.append({"Character Name": name, "Total": rating, "Tank": tank_r, "DPS": dps_r,
                             "Heal": heal_r, "Player Armory": player_url})
        return show

    def check_if_correct_cadd(self, info, channel_id):
        region, realm, character_name, nickname, class_ = info[0].lower(), info[1].lower(), info[2].lower(), info[
            3].lower(), info[4].lower()
        with requests.get(
                f'https://raider.io/api/v1/characters/profile?region={region}&realm={realm}&name={character_name}'
                '&fields=mythic_plus_recent_runs,covenant,gear,raid_progression,'
                'mythic_plus_scores_by_season%3Acurrent') as x:
            if x.status_code != 200:
                return "Not valid information, check what you type! The Right format is:```!cadd eu draenor " \
                       "ceomerlin ceo warlock```"
        player_info = db_.connect_db(channel_id).find(
            {"Region": region, "Realm": realm, "Character Name": character_name})
        try:
            player_info[0]
        except IndexError:
            db_.add_character_to_db(f"{region} {realm} {character_name} {nickname} {class_}")
            return f"```{character_name.capitalize()} has been added to the Data Base!```"
        return f"```{character_name.capitalize()} already exist in the Data Base as:" \
               f"\n{player_info[0]['Region']} {player_info[0]['Realm']} {player_info[0]['Character Name']} " \
               f"{player_info[0]['Player Nickname']} {player_info[0]['Class']}```"

    def check_single_character(self, info):
        region, realm, name = info
        nrun = "0"
        with requests.get(
                f'https://raider.io/api/v1/characters/profile?region={region}&realm={realm}&name={name}&fields'
                f'=mythic_plus_recent_runs,covenant,gear,raid_progression,mythic_plus_scores_by_season%3Acurrent') as\
                x:
            # if x.status_code != 200:
            #     await ctx.send("Not valid information, check what you type!")
            #     return
            name = x.json().get('name')
            c = x.json().get('class')
            spec = x.json().get('active_spec_name')
            tmbn = x.json().get("thumbnail_url")
            ilvl = x.json().get('gear').get('item_level_equipped')
            purl = x.json().get('profile_url')
            nprog = x.json().get('raid_progression').get('sanctum-of-domination').get('normal_bosses_killed')
            hprog = x.json().get('raid_progression').get('sanctum-of-domination').get('heroic_bosses_killed')
            mprog = x.json().get('raid_progression').get('sanctum-of-domination').get('mythic_bosses_killed')
            nsprog = x.json().get('raid_progression').get('sepulcher-of-the-first-ones').get('normal_bosses_killed')
            hsprog = x.json().get('raid_progression').get('sepulcher-of-the-first-ones').get('heroic_bosses_killed')
            msprog = x.json().get('raid_progression').get('sepulcher-of-the-first-ones').get('mythic_bosses_killed')
            score = x.json().get('mythic_plus_scores_by_season')[0].get('scores').get('all')
            if str(score) == str(nrun):
                lfinish = "None"
                keylevel = "0"
                keyup = "0"
                rscore = "0"
            else:
                lfinish = x.json().get('mythic_plus_recent_runs')[0].get('dungeon')
                keylevel = x.json().get('mythic_plus_recent_runs')[0].get('mythic_level')
                keyup = x.json().get('mythic_plus_recent_runs')[0].get('num_keystone_upgrades')
                rscore = x.json().get('mythic_plus_recent_runs')[0].get('score')
            cname = x.json().get('covenant').get('name')
            renown_level = x.json().get('covenant').get("renown_level")
            tank = x.json().get('mythic_plus_scores_by_season')[0].get('scores').get('tank')
            dps = x.json().get('mythic_plus_scores_by_season')[0].get('scores').get('dps')
            healer = x.json().get('mythic_plus_scores_by_season')[0].get('scores').get("healer")
            class_icon = Class_URL.class_icona[c]


ci = CharacterInfo()
