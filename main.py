import datetime
import discord
import os
from discord.ext import commands
from settings import settings

SEASON = settings.WOW_CURRENT_EXPANSION
EXPANSION = settings.WOW_CURRENT_SEASON

UTC = datetime.timezone.utc
times = [datetime.time(hour=x) for x in range(0, 24, 2)]


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(command_prefix="!", help_command=None, intents=intents)

    async def on_ready(self):
        # await client.tree.sync() # once only to sync CRUD slash command
        await self.change_presence(activity=discord.Game(name="Waiting for Sunset"))
        print("Ready")

client = PersistentViewBot()


client.run(os.getenv("TOKEN"))