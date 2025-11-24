import os

class Config:
    # 1. سحب البيانات الحقيقية من ريندر (Render Environment)
    # القيم الافتراضية محطوطة احتياط بس الأساس هو ريندر
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "8297284147:AAHDKI3ncuBhkNq6vLosVujwge5-0Jz8p1A")
    APP_ID = int(os.environ.get("APP_ID", 12345678))
    API_HASH = os.environ.get("API_HASH", "0123456789abcdef0123456789abcdef")
    
    # القنوات (نحولها لأرقام صحيحة)
    try:
        PRIVATE_GROUP_ID = int(os.environ.get("PRIVATE_GROUP_ID", -1003477023425))
        BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", -1003477023425))
        PM_LOGGER_GROUP_ID = int(os.environ.get("PM_LOGGER_GROUP_ID", -1003477023425))
        PRIVATE_GROUP_BOT_API_ID = PRIVATE_GROUP_ID
    except:
        PRIVATE_GROUP_ID = -1003477023425
        BOTLOG_CHATID = -1003477023425
        PM_LOGGER_GROUP_ID = -1003477023425
        PRIVATE_GROUP_BOT_API_ID = -1003477023425

    # 2. الهوية (عشان الملحقات تعرف البوت)
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "Reevs_Bot")
    TG_BOT_USERNAME = os.environ.get("TG_BOT_USERNAME", "Reevs_Bot")
    ALIVE_NAME = os.environ.get("ALIVE_NAME", "Refz User")
    
    # 3. المالك والمطورين (مهم جداً للأوامر)
    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", 7422264678))
    except:
        OWNER_ID = 7422264678
        
    SUDO_USERS = [OWNER_ID]
    
    # 4. المتغيرات اللي كانت ناقصة وتسبب Errors (تمت إضافتها كلها)
    TMP_DOWNLOAD_DIRECTORY = "./downloads/"
    TEMP_DIR = "./downloads/"
    COMMAND_HAND_LER = os.environ.get("COMMAND_HAND_LER", r".")
    SUDO_COMMAND_HAND_LER = os.environ.get("SUDO_COMMAND_HAND_LER", r".")
    
    # 5. متغيرات وهمية (Dummy Vars) لإسكات الملحقات الجائعة
    BOTLOG = True
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
    
    # 6. القوائم والجماليات
    NO_LOAD = []
    UB_BLACK_LIST_CHAT = []
    MAX_MESSAGE_SIZE_LIMIT = 4096
    FINISHED_PROGRESS_STR = "▓"
    UNFINISHED_PROGRESS_STR = "░"
    
    # 7. إنشاء مجلد التحميل لضمان عدم الكراش
    if not os.path.exists(TMP_DOWNLOAD_DIRECTORY):
        try:
            os.makedirs(TMP_DOWNLOAD_DIRECTORY)
        except:
            pass