import os

class Config:
    # ====================================================
    # 1. الثوابت (من ريندر)
    # ====================================================
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", None)
    APP_ID = int(os.environ.get("APP_ID", 12345678))
    API_HASH = os.environ.get("API_HASH", "0123456789abcdef0123456789abcdef")
    
    # القنوات
    try:
        PRIVATE_GROUP_ID = int(os.environ.get("PRIVATE_GROUP_ID", 0))
        BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", PRIVATE_GROUP_ID))
        PM_LOGGER_GROUP_ID = int(os.environ.get("PM_LOGGER_GROUP_ID", PRIVATE_GROUP_ID))
        PRIVATE_GROUP_BOT_API_ID = PRIVATE_GROUP_ID
    except:
        PRIVATE_GROUP_ID = 0
        BOTLOG_CHATID = 0
        PM_LOGGER_GROUP_ID = 0
        PRIVATE_GROUP_BOT_API_ID = 0

    # المالك
    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", 0))
    except:
        OWNER_ID = 0
    SUDO_USERS = [OWNER_ID]
    
    # الهوية
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "Reevs_Bot")
    TG_BOT_USERNAME = os.environ.get("TG_BOT_USERNAME", "Reevs_Bot")
    ALIVE_NAME = "Refz User"

    # ====================================================
    # 2. المتغيرات المفقودة (هنا الحل الجذري)
    # ====================================================
    
    # القوائم
    NO_LOAD = []
    UB_BLACK_LIST_CHAT = []
    
    # المجلدات
    TMP_DOWNLOAD_DIRECTORY = "./downloads/"
    TEMP_DIR = "./downloads/"
    
    # الأوامر
    COMMAND_HAND_LER = os.environ.get("COMMAND_HAND_LER", r".")
    SUDO_COMMAND_HAND_LER = os.environ.get("SUDO_COMMAND_HAND_LER", r".")
    
    # الجماليات (حل مشكلة الضغط)
    MAX_MESSAGE_SIZE_LIMIT = 4096
    FINISHED_PROGRESS_STR = "▓"
    UNFINISHED_PROGRESS_STR = "░"
    BOTLOG = True
    
    # الصور
    THUMB_IMAGE = "https://graph.org/file/5340a83ac9ca428089577.jpg"
    
    # ====================================================
    # 3. مفاتيح API (حل مشكلة SPAMWATCH وربعها)
    # ====================================================
    SPAMWATCH_API = None
    HEROKU_API_KEY = None
    HEROKU_APP_NAME = None
    DEEP_AI = None
    OCR_SPACE_API_KEY = None
    OPENAI_API_KEY = None
    REM_BG_API_KEY = None
    CHROME_DRIVER = None
    GOOGLE_CHROME_BIN = None
    WEATHER_API = None
    VIRUS_API_KEY = None
    ZEDUBLOGO = None

    # التأكد من وجود المجلد
    if not os.path.exists(TMP_DOWNLOAD_DIRECTORY):
        try:
            os.makedirs(TMP_DOWNLOAD_DIRECTORY)
        except:
            pass