from dotenv import dotenv_values, find_dotenv

CONFIG = dotenv_values(find_dotenv())


# CURRENT SEASON AND EXPANSION
WOW_CURRENT_SEASON = 1
WOW_CURRENT_EXPANSION = "TWW"

# DB LOGIN URL
DB_URL = f'postgres://{CONFIG["DB_USER"]}:{CONFIG["DB_PASSWORD"]}@{CONFIG["DB_HOST"]}/{CONFIG["DB_NAME"]}'

# BOT SETTINGS
BOT_TOKEN = CONFIG["TOKEN"]

# SETTINGS RAIDER IO
RAIDER_IO_BASE_URL_FOR_RANK = "https://raider.io/mythic-plus-character-rankings/season"
RAIDER_IO_BASE_URL_FOR_CHARACTER = "https://raider.io/characters"
WOW_API_URL = "https://raider.io/api/v1"
ALTERNATIVE_RUN_FIELDS = "mythic_plus_alternate_runs"
BEST_RUN_FIELDS = "mythic_plus_best_runs"
CURRENT_SEASON_SCORE = "mythic_plus_scores_by_season:current"
RAID_PROGRESSION = "raid_progression"
GEAR = "gear"
MYTHIC_PLUS_RECENT_RUNS = "mythic_plus_recent_runs"
WAITING_TIME = 60
MAX_REQUESTS_PER_MINUTE = 300

# WOW
TOKEN_PICTURE_URL = "https://media.forgecdn.net/avatars/thumbnails/958/807/256/256/638453397304438536.jpeg"
FOOTER_EMBED_PICTURE_URL = "https://static0.gamerantimages.com/wordpress/wp-content/uploads/2024/01/world-of-warcraft-the-war-within-account-wide-reputation-limitation.jpg?q=50&fit=crop&w=400&h=100&dpr=1.5"

# BATTLE NET
BATTLE_CLIENT_ID = CONFIG["BATTLE_CLIENT_ID"]
BATTLE_CLIENT_SECRET = CONFIG["BATTLE_CLIENT_SECRET"]
BATTLE_NET_AUTH_URL = "https://oauth.battle.net/token"


# CHARACTER ADDITION LINKS
WOW_BASE_URL = "https://worldofwarcraft.com/en-"
RAIDBOTS_BASE_URL = "https://www.raidbots.com/simbot/quick?region="
WOW_LOG_BASE_URL = "https://www.warcraftlogs.com/character/"
ARCHON_URL = "https://www.archon.gg/wow/tier-list/dps-rankings/mythic-plus/10/all-dungeons/this-week"

# PICTURES
GEAR_PROGRESSION = "https://raw.githubusercontent.com/ceo-py/Iquit-WoW-Bot/refs/heads/main/pictures/items_progression.png?raw=true"
RANK_THUMBNAIL = "https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/rank_command_thumb.png?raw=true"

# GUIDES LINK
WOWHEAD_SEASON_GEAR_GUIDE = (
    "https://www.wowhead.com/guide/the-war-within/season-1-gearing"
)

# DISCORD
MESSAGE_CHARACTER_LIMIT = 2000

# CHARACTER ROLES
CHARACTER_ROLES = {
    "total": "total_rating",
    "dps": "dps_rating",
    "heal": "healer_rating",
    "tank": "tank_rating",
}
