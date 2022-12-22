import aiohttp
import asyncio
import requests
from data_base_info import DataBaseInfo

db_ = DataBaseInfo()

class_icona = {
    "Warrior": "https://static.wikia.nocookie.net/wowpedia/images/8/83/Inv_sword_27.png/revision/latest/scale-to-width-down/18?cb=20060923064316",
    "Shaman": "https://static.wikia.nocookie.net/wowpedia/images/d/d9/Inv_jewelry_talisman_04.png/revision/latest/scale-to-width-down/18?cb=20060831032254",
    "Demon Hunter": "https://static.wikia.nocookie.net/wowpedia/images/e/e8/ClassIcon_demon_hunter.png/revision/latest/scale-to-width-down/26?cb=20170130100758",
    "Warlock": "https://static.wikia.nocookie.net/wowpedia/images/0/05/Spell_nature_faeriefire.png/revision/latest/scale-to-width-down/18?cb=20070106055518",
    "Druid": "https://static.wikia.nocookie.net/wowpedia/images/c/c8/Inv_misc_monsterclaw_04.png/revision/latest/scale-to-width-down/18?cb=20180222202218",
    "Mage": "https://static.wikia.nocookie.net/wowpedia/images/a/ae/Inv_staff_13.png/revision/latest/scale-to-width-down/18?cb=20070120233003",
    "Death Knight": "https://static.wikia.nocookie.net/wowpedia/images/f/fd/Spell_deathknight_classicon.png/revision/latest/scale-to-width-down/18?cb=20080710164353",
    "Rouge": "https://static.wikia.nocookie.net/wowpedia/images/8/8e/Inv_throwingknife_04.png/revision/latest/scale-to-width-down/18?cb=20060923070701",
    "Hunter": "https://static.wikia.nocookie.net/wowpedia/images/e/e7/Inv_weapon_bow_07.png/revision/latest/scale-to-width-down/18?cb=20060923072423",
    "Paladin": "https://static.wikia.nocookie.net/wowpedia/images/6/6c/Ability_thunderbolt.png/revision/latest/scale-to-width-down/18?cb=20180824003802",
    "Priest": "https://static.wikia.nocookie.net/wowpedia/images/3/3c/Inv_staff_30.png/revision/latest/scale-to-width-down/18?cb=20061011185352",
    "Monk": "https://static.wikia.nocookie.net/wowpedia/images/2/24/Ui-charactercreate-classes_monk.png/revision/latest/scale-to-width-down/64?cb=20111203164429"
}


class CharacterInfo:

    @staticmethod
    def get_data_from_rio(player_info, session):
        raider_io_info = []
        for show in player_info.find({}):
            region, realm, name = show["Region"], show["Realm"], show["Character Name"]
            raider_io_info.append(session.get(
                f'https://raider.io/api/v1/characters/profile?region={region}&realm={realm}&name={name}&fields'
                f'=mythic_plus_recent_runs,covenant,gear,raid_progression,mythic_plus_scores_by_season%3Acurrent'))

        return raider_io_info

    @staticmethod
    async def get_data_for_rank(channel_id: str):
        results = []
        show = []
        data_base = db_.connect_db(channel_id)
        async with aiohttp.ClientSession() as session:
            x = ci.get_data_from_rio(data_base, session)
            responses = await asyncio.gather(*x)
            for response in responses:
                results.append(await response.json())
            # TODO if no such character anymore to remove him from DB and pop msg first time when has been deleted
            for index in results:
                if "error" not in index:
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

    @staticmethod
    def check_if_correct_cadd(info, channel_id):
        region, realm, character_name, nickname, class_ = [x.lower() for x in info]
        with requests.get(
                f'https://raider.io/api/v1/characters/profile?region={region}&realm={realm}&name={character_name}'
                '&fields=mythic_plus_recent_runs,covenant,gear,raid_progression,'
                'mythic_plus_scores_by_season%3Acurrent') as x:
            if x.status_code != 200:
                return "Not valid information, check what you type! The Right format is:```!cadd eu draenor " \
                       "ceomerlin ceo warlock```"

        player_info = db_.connect_db(channel_id).find_one(
            {"$and": [{"Region": region, "Realm": realm, "Character Name": character_name}]})
        if player_info:
            return f"```{character_name.capitalize()} already exist in the Data Base as:" \
                   f"\n{player_info['Region']} {player_info['Realm']} {player_info['Character Name']} " \
                   f"{player_info['Player Nickname']} {player_info['Class']}```"

        db_.add_character_to_db(region, realm, character_name, nickname, class_, channel_id)
        return f"```{character_name.capitalize()} has been added to the Data Base!```"

    @staticmethod
    async def check_single_character(info, channel_id):
        if len(info) == 3:
            region, realm, name = info
        elif len(info) == 2:
            data_base = db_.connect_db(channel_id)
            nickname, player_class = info
            player_found = data_base.find_one({"$and": [{"Player Nickname": nickname}, {"Class": player_class}]})

            if player_found:
                region, realm, name = player_found["Region"], player_found["Realm"], player_found["Character Name"]
            else:
                return

        nrun = "0"
        with requests.get(
                f'https://raider.io/api/v1/characters/profile?region={region}&realm={realm}&name={name}&fields'
                f'=mythic_plus_recent_runs,covenant,gear,raid_progression,mythic_plus_scores_by_season%3Acurrent') as \
                x:
            if x.status_code != 200:
                return
            x = x.json()
            name = x["name"]
            c = x['class']
            spec = x['active_spec_name']
            tmbn = x["thumbnail_url"]
            ilvl = x['gear']['item_level_equipped']
            purl = x['profile_url']
            vault_prog_normal = x['raid_progression']['vault-of-the-incarnates']['normal_bosses_killed']
            vault_prog_heroic = x['raid_progression']['vault-of-the-incarnates']['heroic_bosses_killed']
            vault_prog_mythic = x['raid_progression']['vault-of-the-incarnates']['mythic_bosses_killed']
            score = x['mythic_plus_scores_by_season'][0]['scores']['all']
            if str(score) == str(nrun):
                lfinish = "None"
                keylevel = "0"
                keyup = "0"
                rscore = "0"
            else:
                lfinish = x['mythic_plus_recent_runs'][0]['dungeon']
                keylevel = x['mythic_plus_recent_runs'][0]['mythic_level']
                keyup = x['mythic_plus_recent_runs'][0]['num_keystone_upgrades']
                rscore = x['mythic_plus_recent_runs'][0]['score']
            cname = x['covenant']['name']
            tank = x['mythic_plus_scores_by_season'][0]['scores']['tank']
            dps = x['mythic_plus_scores_by_season'][0]['scores']['dps']
            healer = x['mythic_plus_scores_by_season'][0]['scores']["healer"]
            class_icon = class_icona[c]
        return tmbn, name, spec, c, cname, ilvl, class_icon, tank, dps, healer, vault_prog_normal, vault_prog_heroic, vault_prog_mythic, \
               lfinish, keylevel, keyup, rscore, region, realm, name, score, purl


ci = CharacterInfo()
