
from settings.settings import DB_URL, WOW_API_URL, ALTERNATIVE_RUN_FIELDS, BEST_RUN_FIELDS
import requests
import json

from tortoise.models import Model
from tortoise import fields, Tortoise, run_async
import sys
import os
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)


class Server(Model):
    """
    Server model representing a Discord server.

    Attributes:
    -----------
    id : BigIntField
        Primary key for the server.
    discord_server_id : CharField
        Unique identifier for the Discord server, with a maximum length of 255 characters.
    characters : ManyToManyField
        Many-to-many relationship with the Character model, through the 'characterserver' table.

    Meta:
    -----
    unique_together : tuple
        Ensures that the combination of 'discord_server_id' is unique across the table.
    """
    id = fields.BigIntField(pk=True)
    discord_server_id = fields.CharField(max_length=255, unique=True)
    characters = fields.ManyToManyField(
        'models.Character', related_name='servers', through='characterserver', on_delete=fields.CASCADE
    )

    class Meta:
        unique_together = ('discord_server_id',)


async def create_server(discord_server_id: int) -> Server:
    server = await Server.create(discord_server_id=discord_server_id)
    return server


async def get_server_by_id(server_id: int) -> Server:
    server = await Server.get_or_none(id=server_id)
    return server


async def get_server_by_discord_id(discord_server_id: int) -> Server:
    server = await Server.get_or_none(discord_server_id=discord_server_id)
    return server


async def update_server(server_id: int, discord_server_id: int) -> None:
    await Server.filter(id=server_id).update(discord_server_id=discord_server_id)


async def delete_server(server_id: int) -> None:
    await delete_server_and_associated_data(server_id)

async def delete_server_and_associated_data(server_id: int):
    server = await get_server_by_discord_id(server_id)
    if server:
        characters = await server.characters.all()
        await server.delete()
        for character in characters:
            remaining_servers = await character.servers.all()
            if not remaining_servers:
                await character.delete()


class Character(Model):
    """
    Character model representing a character in a game.

    Attributes:
    -----------
    id : BigIntField
        Primary key for the character.
    region : CharField
        Region where the character is located, with a maximum length of 50 characters.
    realm : CharField
        Realm where the character is located, with a maximum length of 50 characters.
    name : CharField
        Name of the character, with a maximum length of 100 characters.
    character_class : CharField
        Class of the character, with a maximum length of 50 characters.
    total_rating : FloatField
        Total rating of the character.
    dps_rating : FloatField
        DPS (Damage Per Second) rating of the character.
    healer_rating : FloatField
        Healer rating of the character.
    tank_rating : FloatField
        Tank rating of the character.

    Meta:
    -----
    unique_together : tuple
        Ensures that the combination of 'region', 'realm', and 'name' is unique across the table.
    """
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


async def create_character(region: str, realm: str, name: str, character_class: str, total_rating: int, dps_rating: int, healer_rating: int, tank_rating: int) -> Character:
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


async def get_character_by_id(character_id: int) -> Character:
    character = await Character.get_or_none(id=character_id)
    return character


async def get_character_by_region_realm_name(region: str, realm: str, name: str) -> Character:
    character = await Character.get_or_none(region=region, realm=realm, name=name)
    return character


async def update_character(character_id: int, **kwargs: dict) -> None:
    await Character.filter(id=character_id).update(**kwargs)


async def delete_character(character_id: int) -> None:
    await Character.filter(id=character_id).delete()


class CharacterServer(Model):
    """
    CharacterServer model representing the relationship between characters and servers.

    Attributes:
    -----------
    id : BigIntField
        Primary key for the CharacterServer relationship.
    character : ForeignKeyField
        Foreign key to the Character model, with a related name of 'characterservers'.
    server : ForeignKeyField
        Foreign key to the Server model, with a related name of 'characterservers'.
    ranking : IntField
        Ranking of the character on the server.

    Meta:
    -----
    unique_together : tuple
        Ensures that the combination of 'character' and 'server' is unique across the table.
    """
    id = fields.BigIntField(pk=True)
    character = fields.ForeignKeyField(
        'models.Character', related_name='characterservers', on_delete=fields.CASCADE
    )
    server = fields.ForeignKeyField(
        'models.Server', related_name='characterservers', on_delete=fields.CASCADE
    )
    ranking = fields.IntField()

    class Meta:
        unique_together = ('character', 'server')


async def create_character_server(character_id: int, server_id: int, ranking: int) -> CharacterServer:
    character_server = await CharacterServer.create(
        character_id=character_id,
        server_id=server_id,
        ranking=ranking
    )
    return character_server


async def get_character_server_by_id(character_server_id: int) -> CharacterServer:
    character_server = await CharacterServer.get_or_none(id=character_server_id)
    return character_server


async def update_character_server(character_server_id: int, ranking: int) -> CharacterServer:
    await CharacterServer.filter(id=character_server_id).update(ranking=ranking)


async def delete_character_server(character_server_id: int) -> CharacterServer:
    await CharacterServer.filter(id=character_server_id).delete()
# Dungeons


class Dungeon(Model):
    """
    Dungeon model representing a dungeon in a game.

    Attributes:
    -----------
    id : BigIntField
        Primary key for the dungeon.
    name : CharField
        Full name of the dungeon, with a maximum length of 255 characters.
    short_name : CharField
        Short name or abbreviation of the dungeon, with a maximum length of 50 characters.
    icon_discord : CharField
        URL or identifier for the dungeon's icon on Discord, with a maximum length of 255 characters.

    Meta:
    -----
    unique_together : tuple
        Ensures that the combination of 'name' and 'short_name' is unique across the table.
    """
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255)
    short_name = fields.CharField(max_length=50)
    icon_discord = fields.CharField(max_length=255)

    class Meta:
        unique_together = ('name', 'short_name')


async def get_dungeon_by_short_name(short_name: str) -> Dungeon:
    dungeon = await Dungeon.get_or_none(short_name=short_name)
    return dungeon


async def create_dungeon(name: str, short_name: str, icon_discord: str) -> Dungeon:
    dungeon = await Dungeon.create(
        name=name,
        short_name=short_name,
        icon_discord=icon_discord,
    )
    return dungeon


class DungeonRun(Model):
    """
    DungeonRun model representing a run of a dungeon by a character.

    Attributes:
    -----------
    id : BigIntField
        Primary key for the dungeon run.
    character : ForeignKeyField
        Foreign key to the Character model, with a related name of 'dungeon_runs'.
    dungeon : ForeignKeyField
        Foreign key to the Dungeon model, with a related name of 'dungeon_runs'.
    mythic_level : IntField
        Mythic level of the dungeon run.
    num_keystone_upgrades : IntField
        Number of keystone upgrades achieved during the dungeon run.
    clear_time_ms : IntField
        Time taken to clear the dungeon in milliseconds.
    par_time_ms : IntField
        Par time for the dungeon in milliseconds.
    score : FloatField
        Score achieved in the dungeon run.
    affix_type : CharField
        Type of affix applied during the dungeon run, with a maximum length of 50 characters.

    Meta:
    -----
    unique_together : tuple
        Ensures that the combination of 'dungeon', 'character', and 'affix_type' is unique across the table.
    """
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


async def create_dungeon_run(character: str,
                             dungeon: str,
                             mythic_level: int,
                             num_keystone_upgrades: int,
                             clear_time_ms: int,
                             par_time_ms: int,
                             score: int,
                             affix_type: str) -> DungeonRun:
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
