from dotenv import dotenv_values, find_dotenv

CONFIG = dotenv_values(find_dotenv())


# CURRENT SEASON AND EXPANSION
WOW_CURRENT_SEASON = 4
WOW_CURRENT_EXPANSION = "DF"

#DB LOGIN URL
DB_URL = f'postgres://{CONFIG["DB_USER"]}:{CONFIG["DB_PASSWORD"]}@{CONFIG["DB_HOST"]}/{CONFIG["DB_NAME"]}'
