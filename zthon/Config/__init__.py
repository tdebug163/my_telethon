import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Core Telegram Variables (from Render Environment)
    APP_ID = int(os.environ.get("APP_ID", 0))
    API_HASH = os.environ.get("API_HASH")
    ALIVE_NAME = os.environ.get("ALIVE_NAME")
    DB_URI = os.environ.get("DATABASE_URL")
    STRING_SESSION = os.environ.get("STRING_SESSION")
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
    PRIVATE_GROUP_BOT_API_ID = int(os.environ.get("PRIVATE_GROUP_BOT_API_ID", -100))

    # Variables to bypass Heroku-related errors
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", "FAKE_KEY_TO_BYPASS_HEROKU")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", "FAKE_APP_NAME")

    # Variables to fix import/startup errors
    COMMAND_HAND_LER = False
    GENIUS_API_TOKEN = os.environ.get("GENIUS_API_TOKEN", "FAKE_GENIUS_TOKEN")
    UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", "FAKE_UPSTREAM_REPO")
PM_LOGGER_GROUP_ID = int(os.environ.get("PM_LOGGER_GROUP_ID", -100))

class Zedub:
    pass 