from discord import Embed
import os


def load_embeds(bot):
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension(f"embeds.{filename[:-3]}")
