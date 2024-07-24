from dotenv import dotenv_values, find_dotenv

CONFIG = dotenv_values(find_dotenv())


# CURRENT SEASON AND EXPANSION
WOW_CURRENT_SEASON = 4
WOW_CURRENT_EXPANSION = "DF"

#DB LOGIN URL
DB_URL = f'postgres://{CONFIG["DB_USER"]}:{CONFIG["DB_PASSWORD"]}@{CONFIG["DB_HOST"]}/{CONFIG["DB_NAME"]}'

#BOT SETTINGS
BOT_TOKEN = CONFIG["TOKEN"]
BOT_CHANNEL_NAME = CONFIG["DISCORD_CHANNEL_NAME"]

# API SETTINGS RAIDER IO
WOW_API_URL = "https://raider.io/api/v1"
ALTERNATIVE_RUN_FIELDS = "mythic_plus_alternate_runs"
BEST_RUN_FIELDS = "mythic_plus_best_runs"
