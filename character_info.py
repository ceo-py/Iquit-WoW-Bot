import aiohttp
import asyncio
import requests
from database.database import db_, os

class_icons = {
    "Warrior": "https://static.wikia.nocookie.net/wowpedia/images/8/83/Inv_sword_27.png/revision/latest/scale-to-width-down/18?cb=20060923064316",
    "Shaman": "https://static.wikia.nocookie.net/wowpedia/images/d/d9/Inv_jewelry_talisman_04.png/revision/latest/scale-to-width-down/18?cb=20060831032254",
    "Demon Hunter": "https://static.wikia.nocookie.net/wowpedia/images/e/e8/ClassIcon_demon_hunter.png/revision/latest/scale-to-width-down/26?cb=20170130100758",
    "Warlock": "https://static.wikia.nocookie.net/wowpedia/images/0/05/Spell_nature_faeriefire.png/revision/latest/scale-to-width-down/18?cb=20070106055518",
    "Druid": "https://static.wikia.nocookie.net/wowpedia/images/c/c8/Inv_misc_monsterclaw_04.png/revision/latest/scale-to-width-down/18?cb=20180222202218",
    "Mage": "https://static.wikia.nocookie.net/wowpedia/images/a/ae/Inv_staff_13.png/revision/latest/scale-to-width-down/18?cb=20070120233003",
    "Death Knight": "https://static.wikia.nocookie.net/wowpedia/images/f/fd/Spell_deathknight_classicon.png/revision/latest/scale-to-width-down/18?cb=20080710164353",
    "Rogue": "https://static.wikia.nocookie.net/wowpedia/images/8/8e/Inv_throwingknife_04.png/revision/latest/scale-to-width-down/18?cb=20060923070701",
    "Hunter": "https://static.wikia.nocookie.net/wowpedia/images/e/e7/Inv_weapon_bow_07.png/revision/latest/scale-to-width-down/18?cb=20060923072423",
    "Paladin": "https://static.wikia.nocookie.net/wowpedia/images/6/6c/Ability_thunderbolt.png/revision/latest/scale-to-width-down/18?cb=20180824003802",
    "Priest": "https://static.wikia.nocookie.net/wowpedia/images/3/3c/Inv_staff_30.png/revision/latest/scale-to-width-down/18?cb=20061011185352",
    "Monk": "https://static.wikia.nocookie.net/wowpedia/images/e/e2/ClassIcon_monk.png",
}


class CharacterInfo:
    @staticmethod
    def get_battle_net_token() -> str:
        data = {"grant_type": "client_credentials"}

        return requests.post(
            "https://oauth.battle.net/token",
            auth=(os.getenv("BATTLE_CLIENT_ID"), os.getenv("BATTLE_CLIENT_SECRET")),
            data=data,
        ).json()["access_token"]

    @staticmethod
    def get_data_from_rio(player_info, session, backup):
        raider_io_info = []
        if backup:
            token = ci.get_battle_net_token()

        for show in player_info.find({}):
            region, realm, name = show["Region"], show["Realm"], show["Character Name"]

            if not backup:
                raider_io_info.append(
                    session.get(ci.raider_io_api_url(region, realm, name))
                )

            else:
                raider_io_info.append(
                    session.get(ci.battle_net_api_url(region, realm, name, token))
                )

        return raider_io_info

    @staticmethod
    async def get_data_for_rank(channel_id: str, backup) -> list:
        results, show = [], []
        data_base = db_.connect_db(channel_id)
        async with aiohttp.ClientSession() as session:
            x = ci.get_data_from_rio(data_base, session, backup)
            responses = await asyncio.gather(*x)
            for response in responses:
                try:
                    if response.status == 200:
                        results.append(await response.json())
                except:
                    print(f'Error with get data rank response:\n{response}')
                    return 'Error'

            for index in results:
                (name, rating, tank_r, dps_r, heal_r, player_url,) = (
                    ci.raider_io_api(index) if not backup else ci.battle_net_api(index)
                )
                if rating != 0:
                    show.append(
                        {
                            "Character Name": name,
                            "Total": rating,
                            "DPS": dps_r,
                            "Heal": heal_r,
                            "Tank": tank_r,
                            "Player Armory": player_url,
                        }
                    )
        return show

    @staticmethod
    def raider_io_api_url(region, realm, name):
        return (
            f"https://raider.io/api/v1/characters/profile?region={region}&realm={realm}&name={name}&fields"
            f"=mythic_plus_recent_runs,covenant,gear,raid_progression,mythic_plus_scores_by_season%3Acurrent"
        )

    @staticmethod
    def battle_net_api_url(region, realm, name, token):
        return (
            f"https://{region}.api.blizzard.com/profile/wow/character/{realm}/{name}/mythic-keystone-profile?"
            f"namespace=profile-{region}&locale=en_{region.upper()}&access_token={token}"
        )

    @staticmethod
    def raider_io_api(data_json):
        name = data_json["name"]
        rating = int(
            format(
                data_json["mythic_plus_scores_by_season"][0]["segments"]["all"][
                    "score"
                ],
                ".0f",
            )
        )
        tank_r = int(
            format(
                data_json["mythic_plus_scores_by_season"][0]["segments"]["tank"][
                    "score"
                ],
                ".0f",
            )
        )
        dps_r = int(
            format(
                data_json["mythic_plus_scores_by_season"][0]["segments"]["dps"][
                    "score"
                ],
                ".0f",
            )
        )
        heal_r = int(
            format(
                data_json["mythic_plus_scores_by_season"][0]["segments"]["healer"][
                    "score"
                ],
                ".0f",
            )
        )
        player_url = data_json["profile_url"]
        return name, rating, tank_r, dps_r, heal_r, player_url

    @staticmethod
    def character_change_information(channel_id, name, rating, dps_r, heal_r, tank_r):

        db_.update_character_info(
            channel_id,
            name,
            {"Total Rating": rating, "DPS": dps_r, "Healer": heal_r, "Tank": tank_r},
        )

    @staticmethod
    def battle_net_api(data_json):
        name = data_json["character"]["name"]
        if data_json["current_period"]["period"]["id"] == 889:
            rating = (
                int(f"{data_json['current_mythic_rating']['rating']:.0f}")
                if "current_mythic_rating" in data_json
                else 0
            )
        else:
            rating = 0
        tank_r, dps_r, heal_r = 0, 0, 0
        player_url = f"https://worldofwarcraft.com/en-gb/character/eu/{data_json['character']['realm']['slug']}/{name}"
        return name, rating, tank_r, dps_r, heal_r, player_url

    @staticmethod
    async def check_if_correct_cadd(info, channel_id):
        region, realm, character_name, nickname, class_ = [
            x.value.lower() for x in info
        ]
        with requests.get(ci.raider_io_api_url(region, realm, character_name)) as x:
            if x.status_code != 200:
                return (
                    "**Not valid information, check the **[example]"
                    "(https://cdn.discordapp.com/attachments/983670671647313930/1055864102142083154/image.png)"
                )
            real_class = x.json()["class"].lower()
        player_info = await db_.find_character_in_db(
            channel_id, Region=region, Realm=realm, Character_Name=character_name
        )
        if player_info:
            return (
                f"```{character_name.capitalize()} already exist in the database as:"
                f"\n{player_info['Region']} {player_info['Realm']} {player_info['Character Name']} "
                f"{player_info['Player Nickname']} {player_info['Class']}```"
            )

        db_.add_character_to_db(
            region, realm, character_name, nickname, class_, real_class, channel_id
        )
        return f"```{character_name.capitalize()} has been added to the database!```"

    @staticmethod
    async def check_single_character(info, channel_id):
        if len(info) == 3:
            region, realm, name = info
        elif len(info) == 2:
            nickname, player_class = info
            player_found = await db_.find_character_in_db(
                channel_id, Player_Nickname=nickname, Class=player_class
            )

            if player_found:
                region, realm, name = (
                    player_found["Region"],
                    player_found["Realm"],
                    player_found["Character Name"],
                )
            else:
                return

        nrun = "0"
        with requests.get(ci.raider_io_api_url(region, realm, name)) as x:
            if x.status_code != 200:
                return

        x = x.json()
        name = x["name"]
        c = x["class"]
        spec = x["active_spec_name"]
        tmbn = x["thumbnail_url"]
        ilvl = x["gear"]["item_level_equipped"]
        purl = x["profile_url"]
        vault_prog_normal = x["raid_progression"]["aberrus-the-shadowed-crucible"][
            "normal_bosses_killed"
        ]
        vault_prog_heroic = x["raid_progression"]["aberrus-the-shadowed-crucible"][
            "heroic_bosses_killed"
        ]
        vault_prog_mythic = x["raid_progression"]["aberrus-the-shadowed-crucible"][
            "mythic_bosses_killed"
        ]
        score = x["mythic_plus_scores_by_season"][0]["scores"]["all"]
        if str(score) == str(nrun):
            lfinish = "None"
            keylevel = "0"
            keyup = "0"
            rscore = "0"
        else:
            lfinish = x["mythic_plus_recent_runs"][0]["dungeon"]
            keylevel = x["mythic_plus_recent_runs"][0]["mythic_level"]
            keyup = x["mythic_plus_recent_runs"][0]["num_keystone_upgrades"]
            rscore = x["mythic_plus_recent_runs"][0]["score"]
        # cname = x["covenant"]["name"]
        cname = ""
        tank = x["mythic_plus_scores_by_season"][0]["scores"]["tank"]
        dps = x["mythic_plus_scores_by_season"][0]["scores"]["dps"]
        healer = x["mythic_plus_scores_by_season"][0]["scores"]["healer"]
        class_icon = class_icons[c]

        return (
            tmbn,
            name,
            spec,
            c,
            cname,
            ilvl,
            class_icon,
            tank,
            dps,
            healer,
            vault_prog_normal,
            vault_prog_heroic,
            vault_prog_mythic,
            lfinish,
            keylevel,
            keyup,
            rscore,
            region,
            realm,
            name,
            score,
            purl,
        )


ci = CharacterInfo()
