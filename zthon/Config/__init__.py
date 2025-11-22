import os
# Brute force patch to fix missing attributes
from .Config import Config
Config.HEROKU_API_KEY = getattr(Config, 'HEROKU_API_KEY', "FAKE_KEY_TO_BYPASS_HEROKU")
Config.HEROKU_APP_NAME = getattr(Config, 'HEROKU_APP_NAME', "FAKE_APP_NAME")
Config.COMMAND_HAND_LER = getattr(Config, 'COMMAND_HAND_LER', False)
from dotenv import load_dotenv

load_dotenv()

class Config:
    # These are the correct variable names
    APP_ID = int(os.environ.get("APP_ID", 6))
    API_HASH = os.environ.get("API_HASH")
    ALIVE_NAME = os.environ.get("ALIVE_NAME")
    DB_URI = os.environ.get("DATABASE_URL")
    STRING_SESSION = os.environ.get("STRING_SESSION")
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
    PRIVATE_GROUP_BOT_API_ID = int(os.environ.get("PRIVATE_GROUP_BOT_API_ID", -100))
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", "FAKE_KEY_TO_BYPASS_HEROKU")
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", "FAKE_APP_NAME")
COMMAND_HAND_LER = False 
class Zedub:
    pass 