from tortoise import Tortoise
from settings import DB_URL


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
            ]
        },
    )
    await Tortoise.generate_schemas()


# async def close_db():
#     await Tortoise.close_connections()


async def init():
    await init_db()
