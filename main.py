import datetime
import os
import discord
import settings
from discord.ext import commands
from database.db import init_db
from commands import load_commands
from views.add_character_to_server_view import AddCharacterButton


SEASON = settings.WOW_CURRENT_EXPANSION
EXPANSION = settings.WOW_CURRENT_SEASON
BOT_TOKEN = settings.BOT_TOKEN

# UTC = datetime.timezone.utc
# times = [datetime.time(hour=x) for x in range(0, 24, 2)]


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(
            command_prefix="NoCoMaNdS!@#", help_command=None, intents=intents
        )

    async def on_ready(self):
        load_commands(self)

        await self.change_presence(activity=discord.Game(name="M+"))
        await init_db()
        # await self.tree.sync()  # once only to sync CRUD slash command
        # print([
        #     channel.id
        #     for server in self.guilds
        #     for channel in server.channels
        #     if settings.BOT_CHANNEL_NAME in channel.name
        # ])
        print("Ready")

    async def setup_hook(self) -> None:
        self.add_view(AddCharacterButton())


client = PersistentViewBot()


if __name__ == "__main__":
    token = BOT_TOKEN
    if token:
        client.run(token)
    else:
        print("DISCORD_TOKEN environment variable not set")
