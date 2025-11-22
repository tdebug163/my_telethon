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

    # Add other common variables with fake values to prevent future errors
    LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", "FAKE_LYDIA_KEY")
    SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "FAKE_SPOTIFY_ID")
    SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "FAKE_SPOTIFY_SECRET")
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", "FAKE_REMBG_KEY")

class Zedub:
    pass 