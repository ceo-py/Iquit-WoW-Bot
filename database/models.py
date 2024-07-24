import json

from tortoise.models import Model
from tortoise import fields, Tortoise, run_async
import sys
import os
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)
from settings.settings import DB_URL


class Server(Model):
    id = fields.BigIntField(pk=True)
    discord_server_id = fields.CharField(max_length=255, unique=True)
    characters = fields.ManyToManyField(
        'models.Character', related_name='servers', through='character_server')


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
    dungeons_record = fields.JSONField()  # Stores dungeons records as a JSON

    class Meta:
        unique_together = ('region', 'realm', 'name')


async def create_character(region, realm, name, character_class, total_rating, dps_rating, healer_rating, tank_rating, positions=None, dungeons_record=None):
    character = await Character.create(
        region=region,
        realm=realm,
        name=name,
        character_class=character_class,
        total_rating=total_rating,
        dps_rating=dps_rating,
        healer_rating=healer_rating,
        tank_rating=tank_rating,
        positions=positions,
        dungeons_record=dungeons_record
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
        'models.Character', related_name='character_servers')
    server = fields.ForeignKeyField(
        'models.Server', related_name='character_servers')
    ranking = fields.IntField()


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
        dungeons_record={}
    )

    await create_character_server(character_id=character.id, server_id=server.id, ranking=positions)



# active discord server ids
servers = []


async def load_servers(servers):
    os.chdir('database')
    for server in servers:
        with open(f'{server}.json', 'r') as f:
            data = json.load(f)
            for file_data in data:
                await load_character_to_db(server, file_data['Region'], file_data['Realm'], file_data['Character Name'], file_data['Class to display'], file_data['Total Rating'], file_data['DPS'], file_data['Healer'], file_data['Tank'], file_data['Position'], file_data['Dungeons Record'])
                print(f"character create -> {file_data['Character Name']} -> {server}")


async def get_char(region ,realm, name):
    char = await get_character_by_region_realm_name(region, realm, name)
    print(char.id)



# run_async(load_servers(servers))
run_async(get_char('eu', 'draenor', 'ceoheal'))
