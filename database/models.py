
from settings.settings import DB_URL, WOW_API_URL, ALTERNATIVE_RUN_FIELDS, BEST_RUN_FIELDS
import requests
import json

from tortoise.models import Model
from tortoise import fields, Tortoise, run_async
import sys
import os
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)



# Dungeons













# Initialization


async def init():
    await Tortoise.init(
        db_url=DB_URL,
        modules={'models': ['__main__']}
    )
    await Tortoise.generate_schemas()

# Run initialization
run_async(init())


async def load_character_to_db(server_id, region, realm, name, character_class, total_rating, dps_rating, healer_rating, tank_rating, positions, dungeons_record):

    retrieved_server = await get_server_by_discord_id(server_id)
    # Create a new server
    if not retrieved_server:
        server = await create_server(discord_server_id=str(server_id))
    else:
        server = retrieved_server

    # Create a new character

    retrieved_character = await get_character_by_region_realm_name(region, realm, name)
    if retrieved_character:
        print(f"Retrieved Character: {retrieved_character.id}")
        if retrieved_server:
            ret_server = retrieved_server
        else:
            ret_server = server
        await create_character_server(character_id=retrieved_character.id, server_id=ret_server.id, ranking=positions)
        return

    character = await create_character(
        region=region,
        realm=realm,
        name=name,
        character_class=character_class,
        total_rating=total_rating,
        dps_rating=dps_rating,
        healer_rating=healer_rating,
        tank_rating=tank_rating,
    )

    await create_character_server(character_id=character.id, server_id=server.id, ranking=positions)


# active discord server ids
servers = [1116402033684127806, 1053417781879644191, 880161030343376896, 1235704444398866512, 1149694202859507843,
           1055431994437271563, 1234254686752739379, 916420154072662026, 1111731124452990996, 1233099646449094686, 1217065987891789874, 1236256235616079912]


async def load_servers(servers: list[int]):
    os.chdir('database')
    for server in servers:
        with open(f'{server}.json', 'r') as f:
            data = json.load(f)
            for file_data in data:
                try:
                    await load_character_to_db(server, file_data['Region'], file_data['Realm'], file_data['Character Name'], file_data['Class to display'], file_data['Total Rating'], file_data['DPS'], file_data['Healer'], file_data['Tank'], file_data['Position'], file_data['Dungeons Record'])
                    print(
                        f"character create -> {file_data['Character Name']} -> {server}")
                except Exception as e:
                    print(e)


async def get_char(region: str, realm: str, name: str):
    char = await get_character_by_region_realm_name(region, realm, name)
    print(char.id)


async def load_dungeons(current_dungeons: list[dict]) -> None:
    for dungeon in current_dungeons:
        name = dungeon['name']
        short_name = dungeon['short_name']
        icon_discord = dungeon['icon_discord']
        await create_dungeon(name, short_name, icon_discord)
        print(f'{name} -> {short_name} -> {icon_discord}')


async def load_character_information(character_id: int):
    character = await get_character_by_id(character_id)
    with requests.get(f'{WOW_API_URL}/characters/profile?region={character.region}&realm={character.realm}&name={character.name}&fields={ALTERNATIVE_RUN_FIELDS},{BEST_RUN_FIELDS}') as response:
        data = response.json()

        try:
            # for alter in data['mythic_plus_alternate_runs']:
            for alter in data['mythic_plus_best_runs']:
                dungeon = await get_dungeon_by_short_name(alter['short_name'].lower())
                affix_type = alter['affixes'][0]['name']

                # Prepare dictionary with all required parameters
                dungeon_run_data = {
                    "character": character,
                    "dungeon": dungeon,
                    "mythic_level": alter['mythic_level'],
                    "num_keystone_upgrades": alter['num_keystone_upgrades'],
                    "clear_time_ms": alter['clear_time_ms'],
                    "par_time_ms": alter['par_time_ms'],
                    "score": alter['score'],
                    "affix_type": affix_type,
                }
                # Call create_dungeon_run with unpacked dictionary
                await create_dungeon_run(**dungeon_run_data)
        except Exception as e:
            print(e)


# run_async(load_servers(servers))
run_async(load_dungeons(current_dungeons))
# for id in range(1, 247):
# run_async(load_character_information(id))
