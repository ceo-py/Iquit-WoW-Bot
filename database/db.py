import json
from tortoise import Tortoise
from settings import DB_URL
from .service.emojis_discord_service import create_emoji
from .service.dungeon_service import create_dungeon


async def init_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={
            "models": [
                "database.models.character_server",
                "database.models.character",
                "database.models.dungeon_run",
                "database.models.dungeon",
                "database.models.server",
                "database.models.emojis_discord",
            ]
        },
    )
    await Tortoise.generate_schemas()


async def load_initial_data():
    emojis_to_load = (
        {
            "file name": "affixdiscordicons",
            "type": "Affix",
        },
        {
            "file name": "characterdiscordicons",
            "type": "Character",
        },
        {
            "file name": "characterrolediscordicons",
            "type": "Character_Role",
        },
        {
            "file name": "commondiscordicons",
            "type": "Common",
        },
        {
            "file name": "dungeondiscordicons",
            "type": "Dungeon",
        },
        {
            "file name": "regiondiscordicons",
            "type": "Region",
        },
    )
    for emoji in emojis_to_load:
        file_name = emoji.get("file name")

        with open(f"icons/{file_name}/{file_name}.json", "r") as file:
            emojis_discord_data = json.load(file)

            for name, data in emojis_discord_data.items():
                emoji_type = emoji.get("type")

                await create_emoji(name, data, emoji_type)
                if emoji_type != "Dungeon":
                    continue
                await create_dungeon(name, data.split(":")[1])


# async def close_db():
#     await Tortoise.close_connections()


async def init():
    await init_db()
