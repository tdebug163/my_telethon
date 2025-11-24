import sys
import os
import glob
import asyncio
import logging
import types
from pathlib import Path
from telethon import Button, functions, types as tele_types, utils

# ==============================================================================
# mikey: 🛑 الدستور الصارم (Strict Config) - لإصلاح الأوامر 🛑
# ==============================================================================
print("mikey: ☠️ جاري تحميل الإعدادات العسكرية (بدون سحر)...")

# 1. بياناتك (تأكد منها 100%)
MY_TOKEN = "8297284147:AAHDKI3ncuBhkNq6vLosVujwge5-0Jz8p1A"
MY_CHANNEL = -1003477023425
MY_ID = 7422264678

# 2. زرع القيم في البيئة (خط الدفاع الأول)
os.environ["TG_BOT_TOKEN"] = MY_TOKEN
os.environ["PRIVATE_GROUP_ID"] = str(MY_CHANNEL)
os.environ["BOTLOG_CHATID"] = str(MY_CHANNEL)
os.environ["BOT_USERNAME"] = "Reevs_Bot"
os.environ["OWNER_ID"] = str(MY_ID)

if not os.path.exists("./downloads/"):
    try: os.makedirs("./downloads/")
    except: pass

# 3. الكلاس الصريح (بدون __getattr__)
# لازم نعرف كل شي يحتاجه السورس هنا بوضوح
class StrictConfig:
    # --- الأساسيات ---
    TG_BOT_TOKEN = MY_TOKEN
    APP_ID = 12345678
    API_HASH = "0123456789abcdef0123456789abcdef"
    
    # --- القنوات ---
    PRIVATE_GROUP_ID = MY_CHANNEL
    PRIVATE_GROUP_BOT_API_ID = MY_CHANNEL
    BOTLOG = True
    BOTLOG_CHATID = MY_CHANNEL
    PM_LOGGER_GROUP_ID = MY_CHANNEL
    
    # --- الهوية ---
    BOT_USERNAME = "Reevs_Bot"
    TG_BOT_USERNAME = "Reevs_Bot"
    ALIVE_NAME = "Refz User"
    
    # --- الأوامر (هنا مربط الفرس لإصلاح العطل) ---
    # لازم تكون Raw String
    COMMAND_HAND_LER = r"\." 
    SUDO_COMMAND_HAND_LER = r"\."
    
    # --- الصلاحيات ---
    OWNER_ID = MY_ID
    SUDO_USERS = [MY_ID] # قائمة المطورين
    
    # --- المجلدات ---
    TMP_DOWNLOAD_DIRECTORY = "./downloads/"
    TEMP_DIR = "./downloads/"
    
    # --- قوائم ومتغيرات أخرى تطلبها الملحقات ---
    NO_LOAD = []
    UB_BLACK_LIST_CHAT = []
    MAX_MESSAGE_SIZE_LIMIT = 4096
    
    # --- مفاتيح وهمية (عشان الملحقات ما تكرش) ---
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

# 4. الحقن المباشر في الذاكرة
sys.modules["zthon.Config"] = type("ConfigModule", (object,), {"Config": StrictConfig})
sys.modules["zthon.configs"] = type("ConfigModule", (object,), {"Config": StrictConfig})
sys.modules["Config"] = StrictConfig

# تعديل الكلاس الأصلي لو موجود (زيادة تأكيد)
try:
    from zthon.Config import Config as Original
    for key, value in StrictConfig.__dict__.items():
        if not key.startswith("__"):
            setattr(Original, key, value)
except:
    pass

print("mikey: ✅ تم تثبيت الدستور. الأوامر (.) جاهزة.")

# ==============================================================================

from ..core.logger import logging
from ..core.session import zedub
from ..helpers.utils import install_pip
from ..helpers.utils.utils import runcmd
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar
from .pluginmanager import load_module
from .tools import create_supergroup

ENV = bool(os.environ.get("ENV", False))
LOGS = logging.getLogger("zthon")
cmdhr = StrictConfig.COMMAND_HAND_LER 

if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]

bot = zedub

# متغير لمنع التكرار
STARTUP_DONE = False

# ==============================================================================

async def setup_bot():
    print(f"mikey: ✅ البوت جاهز.")
    return

async def startupmessage():
    """
    رسالة البدء (مرة واحدة فقط)
    """
    global STARTUP_DONE
    if STARTUP_DONE:
        return

    try:
        if StrictConfig.BOTLOG:
            try:
                await zedub.tgbot.send_file(
                    StrictConfig.BOTLOG_CHATID,
                    "https://graph.org/file/5340a83ac9ca428089577.jpg",
                    caption=f"**•⎆┊تـم بـدء تشغـيل سـورس ريفز 🧸♥️**\n✅ الأوامر مفعلة: `.`",
                    buttons=[(Button.url("Source", "https://t.me/def_Zoka"),)],
                )
                STARTUP_DONE = True # قفلنا الباب
            except Exception as e:
                print(f"mikey: القناة مقفلة ({e})")
    except:
        pass
    
    # تحديثات الريستارت
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
            await zedub.check_testcases()
            # هنا نستخدم edit_message عشان نعرف انه اشتغل
            await zedub.edit_message(msg_details[0], msg_details[1], "**•⎆┊تـم إعـادة تشغيـل السـورس وتفعيل الأوامر ✅**")
            del_keyword_collectionlist("restart_update")
    except:
        pass

async def mybot():
    pass

async def add_bot_to_logger_group(chat_id):
    pass

zthon = {"@def_Zoka", "@refz_var", "@KALAYISH", "@senzir2", "rev_fxx"}

async def saves():
    pass

async def load_plugins(folder, extfolder=None):
    """
    تحميل الملحقات (مع الرسايل العربية)
    """
    if extfolder:
        path = f"{extfolder}/*.py"
        plugin_path = extfolder
    else:
        path = f"zthon/{folder}/*.py"
        plugin_path = f"zthon/{folder}"

    files = glob.glob(path)
    files.sort()
    success = 0
    failure = []

    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            try:
                if (pluginname not in StrictConfig.NO_LOAD) and (
                    pluginname not in VPS_NOLOAD
                ):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            # هنا اللحظة الحاسمة: التحميل باستخدام الكونفيج الجديد
                            load_module(
                                pluginname,
                                plugin_path=plugin_path,
                            )
                            if shortname in failure:
                                failure.remove(shortname)
                            success += 1
                            LOGS.info(f"تـم تثبيت ملـف {shortname}")
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                        except AttributeError as ae:
                            # لو طلع خطأ هنا يعني نسينا متغير في StrictConfig
                            LOGS.info(f"متغير ناقص في {shortname}: {ae}")
                            failure.append(shortname)
                            break
                        except Exception as e:
                            LOGS.info(f"فشل {shortname}: {e}")
                            failure.append(shortname)
                            break
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                LOGS.info(f"خطأ في الملف {shortname}: {e}")

    if extfolder:
        if not failure:
            failure.append("None")
        try:
            await zedub.tgbot.send_message(
                StrictConfig.BOTLOG_CHATID,
                f'Ext Plugins: `{success}`\nFailed: `{", ".join(failure)}`',
            )
        except:
            pass

async def verifyLoggerGroup():
    try:
        addgvar("PRIVATE_GROUP_BOT_API_ID", MY_CHANNEL)
        addgvar("PM_LOGGER_GROUP_ID", MY_CHANNEL)
    except:
        pass
    return

async def install_externalrepo(repo, branch, cfolder):
    pass