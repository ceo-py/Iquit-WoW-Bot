from dotenv import dotenv_values, find_dotenv

CONFIG = dotenv_values(find_dotenv())


# CURRENT SEASON AND EXPANSION
WOW_CURRENT_SEASON = CONFIG["WOW_CURRENT_SEASON"]
WOW_CURRENT_EXPANSION = CONFIG["WOW_CURRENT_EXPANSION"]

# DB LOGIN URL
DB_URL = f'postgres://{CONFIG["DB_USER"]}:{CONFIG["DB_PASSWORD"]}@{CONFIG["DB_HOST"]}/{CONFIG["DB_NAME"]}'

# BOT SETTINGS
BOT_TOKEN = CONFIG["TOKEN"]
BOT_CHANNEL_NAME = CONFIG["DISCORD_CHANNEL_NAME"]

# SETTINGS RAIDER IO
RAIDER_IO_BASE_URL_FOR_RANK = "https://raider.io/mythic-plus-character-rankings/season"
WOW_API_URL = "https://raider.io/api/v1"
ALTERNATIVE_RUN_FIELDS = CONFIG["ALTERNATIVE_RUN_FIELDS"]
BEST_RUN_FIELDS = CONFIG["BEST_RUN_FIELDS"]
CURRENT_SEASON_SCORE = CONFIG["CURRENT_SEASON_SCORE"]
RAID_PROGRESSION = CONFIG["RAID_PROGRESSION"]
GEAR = CONFIG["GEAR"]
MYTHIC_PLUS_RECENT_RUNS = CONFIG["MYTHIC_PLUS_RECENT_RUNS"]
SLEEPING_TIME = 69
CHUNK_SIZE = 300

# WOW
TOKEN_PICTURE_URL = CONFIG["TOKEN_PICTURE_URL"]
FOOTER_EMBED_PICTURE_URL = CONFIG["FOOTER_EMBED_PICTURE_URL"]

# BATTLE NET
BATTLE_CLIENT_ID = CONFIG["BATTLE_CLIENT_ID"]
BATTLE_CLIENT_SECRET = CONFIG["BATTLE_CLIENT_SECRET"]
BATTLE_NET_AUTH_URL = "https://oauth.battle.net/token"


# CHARACTER ADDITION LINKS
WOW_BASE_URL = CONFIG["WOW_BASE_URL"]
RAIDBOTS_BASE_URL = CONFIG["RAIDBOTS_BASE_URL"]
WOW_LOG_BASE_URL = CONFIG["WOW_LOG_BASE_URL"]
ARCHON_URL = "https://www.archon.gg/wow/tier-list/dps-rankings/mythic-plus/10/all-dungeons/this-week"

# PICTURES
GEAR_PROGRESSION = CONFIG["GEAR_PROGRESSION"]
RANK_THUMBNAIL = "https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/rank_command_thumb.png?raw=true"

# GUIDES LINK
WOWHEAD_SEASON_GEAR_GUIDE = CONFIG["WOWHEAD_SEASON_GEAR_GUIDE"]
