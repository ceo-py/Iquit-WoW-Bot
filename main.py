import datetime
import os
import discord
import settings
from discord.ext import commands
from database.db import init_db
from commands  import load_commands

from database.service.character_service import get_character_by_region_realm_name

SEASON = settings.WOW_CURRENT_EXPANSION
EXPANSION = settings.WOW_CURRENT_SEASON
BOT_TOKEN = settings.BOT_TOKEN

# UTC = datetime.timezone.utc
# times = [datetime.time(hour=x) for x in range(0, 24, 2)]


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(command_prefix="!", help_command=None, intents=intents)

    async def on_ready(self):
        # await client.tree.sync() # once only to sync CRUD slash command
        await self.change_presence(activity=discord.Game(name="M+"))
        await init_db()
        # print([
        #     channel.id
        #     for server in self.guilds
        #     for channel in server.channels
        #     if settings.BOT_CHANNEL_NAME in channel.name
        # ])
        print("Ready")


client = PersistentViewBot()
load_commands(client)


if __name__ == "__main__":
    token = BOT_TOKEN
    if token:
        client.run(token)
    else:
        print("DISCORD_TOKEN environment variable not set")
