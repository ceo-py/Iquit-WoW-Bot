import sys
import os
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)

from settings.settings import DB_URL
from tortoise import fields, Tortoise, run_async
from tortoise.models import Model




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
    positions = fields.JSONField()  # Stores server-specific positions as a JSON
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
    ranking = fields.FloatField()


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


# Example usage
async def example_usage():
    # Create a new server
    server = await create_server(discord_server_id='123456789011')

    # Create a new character
    character = await create_character(
        region='US11',
        realm='RealmName',
        name='CharacterName',
        character_class='Warrior',
        total_rating=1500,
        dps_rating=1600,
        healer_rating=1400,
        tank_rating=0,
        positions={'server_id1': 2, 'server_id2': 1},
        dungeons_record={'Tyrannical': {'Neltharus': {'mythic_level': 13, 'short_name': 'NLT',
                                                      'clear_time_ms': 1903505, 'par_time_ms': 1980999, 'score': 191.5}}}
    )

    # Create a new character-server relationship
    character_server = await create_character_server(character_id=character.id, server_id=server.id, ranking=1.5)

    # Retrieve a character by ID
    retrieved_character = await get_character_by_id(character.id)
    if retrieved_character:
        print(f"Retrieved Character: {retrieved_character.id}")

    # # Update a character's ratings
    # await update_character(character_id=character.id, dps_rating=1700)

    # # Delete a character-server relationship
    # await delete_character_server(character_server.id)

    # # Delete a server
    # await delete_server(server.id)

# Run the example usage (in an asyncio context)
# run_async(example_usage())


# async def example_debug():
#     character_id = 1  # Update with the actual character ID you want to retrieve
#     retrieved_character = await get_character_by_id(character_id)
    
#     if retrieved_character:
#         print(f"Retrieved Character: {retrieved_character.positions}")
#     else:
#         print(f"Character with ID {character_id} not found.")

# run_async(example_debug())
