import datetime
import discord
import settings
from discord.ext import commands, tasks
from database.db import init_db, load_initial_data
from utils.scheduler.scheduler import task_scheduler
from commands import load_commands
from views.buttons_character_statistics import ButtonsCharacterStatistics
from utils.emojis import get_emojis


SEASON = settings.WOW_CURRENT_EXPANSION
EXPANSION = settings.WOW_CURRENT_SEASON
BOT_TOKEN = settings.BOT_TOKEN

UTC = datetime.timezone.utc
times = [
    datetime.time(hour=h, minute=m)
    for h in range(24)
    for m in range(0, 60, settings.SCHEDULER_INTERVAL_MINUTES)
]


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()

        self.affix_emojis = None
        self.character_emojis = None
        self.common_emojis = None
        self.dungeon_emojis = None
        self.region_emojis = None
        self.character_role_emojis = None

        super().__init__(
            command_prefix="NoCoMmAnDs!@#", help_command=None, intents=intents
        )

    async def load_emojis(self):
        emoji_categories = [
            "Affix",
            "Character",
            "Common",
            "Dungeon",
            "Region",
            "Character_Role",
        ]

        for category in emoji_categories:
            setattr(self, f"{category.lower()}_emojis", await get_emojis(category))

    @tasks.loop(time=times)
    async def scheduler_rio_every_15_minutes(self):
        print("Scheduler started")
        await task_scheduler()

    async def on_ready(self):
        load_commands(self)

        await self.change_presence(activity=discord.Game(name="M+"))
        await init_db()

        # use only for initial data loading when first time creating database make sure you update json files in icons folder
        await load_initial_data()

        await self.load_emojis()
        print("Ready")
        # await task_scheduler()
        # await self.scheduler_rio_every_15_minutes.start()
        # await self.tree.sync()  # once only to sync CRUD slash command
        # print([
        #     channel.id
        #     for server in self.guilds
        #     for channel in server.channels
        #     if settings.BOT_CHANNEL_NAME in channel.name
        # ])

    async def setup_hook(self) -> None:
        self.add_view(ButtonsCharacterStatistics())


client = PersistentViewBot()


if __name__ == "__main__":
    token = BOT_TOKEN
    if token:
        client.run(token)
    else:
        print("DISCORD_TOKEN environment variable not set")
