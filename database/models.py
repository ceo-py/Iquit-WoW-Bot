
import requests
import json

from tortoise.models import Model
from tortoise import fields, Tortoise, run_async
import sys
import os
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)
from settings.settings import DB_URL, WOW_API_URL, ALTERNATIVE_RUN_FIELDS, BEST_RUN_FIELDS


class Server(Model):
    id = fields.BigIntField(pk=True)
    discord_server_id = fields.CharField(max_length=255, unique=True)
    characters = fields.ManyToManyField(
        'models.Character', related_name='servers', through='characterserver')
    
    class Meta:
        unique_together = ('discord_server_id',)


async def create_server(discord_server_id):
    server = await Server.create(discord_server_id=discord_server_id)
    return server


async def get_server_by_id(server_id):
    server = await Server.get_or_none(id=server_id)
    return server


async def get_server_by_discord_id(discord_server_id):
    server = await Server.get_or_none(discord_server_id=discord_server_id)
    return server


async def update_server(server_id, discord_server_id):
    await Server.filter(id=server_id).update(discord_server_id=discord_server_id)


async def delete_server(server_id):
    await Server.filter(id=server_id).delete()


class Character(Model):
    id = fields.BigIntField(pk=True)
    region = fields.CharField(max_length=50)
    realm = fields.CharField(max_length=50)
    name = fields.CharField(max_length=100)
    character_class = fields.CharField(max_length=50)
    total_rating = fields.FloatField()
    dps_rating = fields.FloatField()
    healer_rating = fields.FloatField()
    tank_rating = fields.FloatField()

    class Meta:
        unique_together = ('region', 'realm', 'name')


async def create_character(region, realm, name, character_class, total_rating, dps_rating, healer_rating, tank_rating):
    character = await Character.create(
        region=region,
        realm=realm,
        name=name,
        character_class=character_class,
        total_rating=total_rating,
        dps_rating=dps_rating,
        healer_rating=healer_rating,
        tank_rating=tank_rating,
    )
    return character


async def get_character_by_id(character_id):
    character = await Character.get_or_none(id=character_id)
    return character


async def get_character_by_region_realm_name(region, realm, name):
    character = await Character.get_or_none(region=region, realm=realm, name=name)
    return character


async def update_character(character_id, **kwargs):
    await Character.filter(id=character_id).update(**kwargs)


async def delete_character(character_id):
    await Character.filter(id=character_id).delete()


class CharacterServer(Model):
    id = fields.BigIntField(pk=True)
    character = fields.ForeignKeyField(
        'models.Character', related_name='characterservers')
    server = fields.ForeignKeyField(
        'models.Server', related_name='characterservers')
    ranking = fields.IntField()

    class Meta:
        unique_together = ('character', 'server')


async def create_character_server(character_id, server_id, ranking):
    character_server = await CharacterServer.create(
        character_id=character_id,
        server_id=server_id,
        ranking=ranking
    )
    return character_server


async def get_character_server_by_id(character_server_id):
    character_server = await CharacterServer.get_or_none(id=character_server_id)
    return character_server


async def update_character_server(character_server_id, ranking):
    await CharacterServer.filter(id=character_server_id).update(ranking=ranking)


async def delete_character_server(character_server_id):
    await CharacterServer.filter(id=character_server_id).delete()

current_dungeons = [
    {"name": "Ara-Kara, City of Echoes",
     "short_name": "arak",
     "icon_discord": "<:arak:1267431668071792701>"},
    {"name": "City of Threads",
     "short_name": "cot",
     "icon_discord": "<:cot:1267431653249126462>"},
    {"name": "Grim Batol",
     "short_name": "gb",
     "icon_discord": "<:gb:1267431531807506525>"},
    {"name": "Mists of Tirna Scithe",
     "short_name": "mists",
     "icon_discord": "<:mists:1267431596437536871>"},
    {"name": "Siege of Boralus",
     "short_name": "siege",
     "icon_discord": "<:siege:1267431561691795497>"},
    {"name": "The Dawnbreaker",
     "short_name": "dawn",
     "icon_discord": "<:dawn:1267431616003833943>"},
    {"name": "The Necrotic Wake",
     "short_name": "nw",
     "icon_discord": "<:nw:1267431579647606785>"},
    {"name": "The Stonevault",
     "short_name": "sv",
     "icon_discord": "<:sv:1267431637570945034>"},
]
current_affixes = {
    "tyrannical": "<:tyrannical:1239631772526973018>",
    "fortified": "<:fortified:1239631756517314624>",
}

# Dungeons


class Dungeon(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255)
    short_name = fields.CharField(max_length=50)
    icon_discord = fields.CharField(max_length=255)

    class Meta:
        unique_together = ('name', 'short_name')


async def get_dungeon_by_short_name(short_name):
    dungeon = await Dungeon.get_or_none(short_name=short_name)
    return dungeon


async def create_dungeon(name, short_name, icon_discord):
    dungeon = await Dungeon.create(
        name=name,
        short_name=short_name,
        icon_discord=icon_discord,
    )
    return dungeon


class DungeonRun(Model):
    id = fields.BigIntField(pk=True)
    character = fields.ForeignKeyField(
        'models.Character', related_name='dungeon_runs')
    dungeon = fields.ForeignKeyField(
        'models.Dungeon', related_name='dungeon_runs')
    mythic_level = fields.IntField()
    num_keystone_upgrades = fields.IntField()
    clear_time_ms = fields.IntField()
    par_time_ms = fields.IntField()
    score = fields.FloatField()
    affix_type = fields.CharField(max_length=50)
    class Meta:
        unique_together = ('dungeon', 'character', 'affix_type')


async def create_dungeon_run(character,
                             dungeon,
                             mythic_level,
                             num_keystone_upgrades,
                             clear_time_ms,
                             par_time_ms,
                             score,
                             affix_type):
    dungeon = await DungeonRun.create(
        character=character,
        dungeon=dungeon,
        mythic_level=mythic_level,
        num_keystone_upgrades=num_keystone_upgrades,
        clear_time_ms=clear_time_ms,
        par_time_ms=par_time_ms,
        score=score,
        affix_type=affix_type,
    )
    return dungeon

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


async def load_servers(servers):
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


async def get_char(region, realm, name):
    char = await get_character_by_region_realm_name(region, realm, name)
    print(char.id)


async def load_dungeons(current_dungeons):
    for dungeon in current_dungeons:
        name = dungeon['name']
        short_name = dungeon['short_name']
        icon_discord = dungeon['icon_discord']
        await create_dungeon(name, short_name, icon_discord)
        print(f'{name} -> {short_name} -> {icon_discord}')


async def load_character_information(character_id):
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

