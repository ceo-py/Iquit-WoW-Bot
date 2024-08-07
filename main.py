import datetime
import discord
from discord.ext import commands
from settings import settings

SEASON = settings.WOW_CURRENT_EXPANSION
EXPANSION = settings.WOW_CURRENT_SEASON
BOT_TOKEN = settings.BOT_TOKEN

UTC = datetime.timezone.utc
times = [datetime.time(hour=x) for x in range(0, 24, 2)]


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(command_prefix="!", help_command=None, intents=intents)

    async def on_ready(self):
        # await client.tree.sync() # once only to sync CRUD slash command
        await self.change_presence(activity=discord.Game(name="Waiting for Sunset"))
        # print([
        #     channel.id
        #     for server in self.guilds
        #     for channel in server.channels
        #     if settings.BOT_CHANNEL_NAME in channel.name
        # ])
        print("Ready")


client = PersistentViewBot()


client.run(BOT_TOKEN)
