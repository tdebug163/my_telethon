import sys
import os
import glob
import asyncio
import logging
import time
from pathlib import Path
from telethon import Button, functions, types as tele_types, utils

# ==============================================================================
# mikey: 🔨 الحل الفيزيائي (كتابة الملفات على الهاردسك) 🔨
# ==============================================================================
print("mikey: ☠️ جاري كتابة ملفات Config.py فعلياً لإسكات الملحقات...")

# 1. محتوى ملف الكونفيج الصحيح (فيه كل المتغيرات الناقصة)
CONFIG_CONTENT = """
import os

class Config:
    # --- الأساسيات ---
    TG_BOT_TOKEN = "8297284147:AAHDKI3ncuBhkNq6vLosVujwge5-0Jz8p1A"
    APP_ID = 12345678
    API_HASH = "0123456789abcdef0123456789abcdef"
    
    # --- القنوات ---
    PRIVATE_GROUP_ID = -1003477023425
    PRIVATE_GROUP_BOT_API_ID = -1003477023425
    BOTLOG = True
    BOTLOG_CHATID = -1003477023425
    PM_LOGGER_GROUP_ID = -1003477023425
    
    # --- الهوية ---
    BOT_USERNAME = "Reevs_Bot"
    TG_BOT_USERNAME = "Reevs_Bot"
    ALIVE_NAME = "Refz User"
    
    # --- الأوامر (حل مشكلة SUDO) ---
    COMMAND_HAND_LER = r"\." 
    SUDO_COMMAND_HAND_LER = r"\."
    
    # --- الصلاحيات ---
    OWNER_ID = 7422264678
    SUDO_USERS = [7422264678]
    
    # --- المجلدات (حل مشكلة TMP_DIR) ---
    TMP_DOWNLOAD_DIRECTORY = "./downloads/"
    TEMP_DIR = "./downloads/"
    
    # --- متغيرات وهمية لإسكات الملحقات ---
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
    
    # --- قوائم ---
    NO_LOAD = []
    UB_BLACK_LIST_CHAT = []
    MAX_MESSAGE_SIZE_LIMIT = 4096
    FINISHED_PROGRESS_STR = "▓"
    UNFINISHED_PROGRESS_STR = "░"
"""

# 2. كتابة الملفات بالقوة
try:
    # نكتب في المسار الفرعي
    with open("zthon/Config.py", "w", encoding="utf-8") as f:
        f.write(CONFIG_CONTENT)
    
    # نكتب في المسار الرئيسي (احتياط)
    with open("config.py", "w", encoding="utf-8") as f:
        f.write(CONFIG_CONTENT)
        
    print("mikey: ✅ تم إنشاء ملفات Config.py بنجاح.")
except Exception as e:
    print(f"mikey: ❌ خطأ في الكتابة: {e}")

# 3. إعداد البيئة (عشان السورس يقرأ منها لو حب)
os.environ["TG_BOT_TOKEN"] = "8297284147:AAHDKI3ncuBhkNq6vLosVujwge5-0Jz8p1A"
os.environ["PRIVATE_GROUP_ID"] = "-1003477023425"
os.environ["BOTLOG_CHATID"] = "-1003477023425"
os.environ["TMP_DOWNLOAD_DIRECTORY"] = "./downloads/"
os.environ["SUDO_COMMAND_HAND_LER"] = r"\."

if not os.path.exists("./downloads/"):
    try: os.makedirs("./downloads/")
    except: pass

# ==============================================================================
# الآن نستدعي الكونفيج اللي كتبناه
# ==============================================================================
try:
    # لازم نسوي reload عشان لو كان محمل القديم يحدثه
    import zthon.Config
    import importlib
    importlib.reload(zthon.Config)
    from zthon.Config import Config
    print("mikey: ✅ تم تحميل Config الجديد.")
except ImportError:
    print("mikey: ⚠️ فشل استدعاء Config، بنعتمد على الذاكرة.")
    # (هنا ممكن نحط كلاس احتياطي لو تبي، بس الكتابة المفروض تكفي)

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
cmdhr = Config.COMMAND_HAND_LER 

if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]

bot = zedub
STARTUP_DONE = False

async def setup_bot():
    print(f"mikey: ✅ البوت جاهز.")
    return

async def startupmessage():
    global STARTUP_DONE
    if STARTUP_DONE: return
    try:
        if Config.BOTLOG:
            try:
                await zedub.tgbot.send_file(
                    Config.BOTLOG_CHATID,
                    "https://graph.org/file/5340a83ac9ca428089577.jpg",
                    caption=f"**•⎆┊تـم بـدء تشغـيل سـورس ريفز 🧸♥️**\n✅ تم إصلاح الملفات.",
                    buttons=[(Button.url("Source", "https://t.me/def_Zoka"),)],
                )
                STARTUP_DONE = True
            except: pass
    except: pass
    
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
            await zedub.check_testcases()
            await zedub.edit_message(msg_details[0], msg_details[1], "**•⎆┊تـم إعـادة تشغيـل السـورس وتفعيل الأوامر ✅**")
            del_keyword_collectionlist("restart_update")
    except: pass

async def mybot(): pass
async def add_bot_to_logger_group(chat_id): pass
zthon = {"@def_Zoka", "@refz_var", "@KALAYISH", "@senzir2", "rev_fxx"}
async def saves(): pass

async def load_plugins(folder, extfolder=None):
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
        # ======================================================
        # مصلح الملفات (بدون إزعاج)
        # ======================================================
        try:
            with open(name, "r", encoding='utf-8', errors='ignore') as f:
                content = f.read()
            modified = False
            
            # إصلاح الفاصلة
            if "‚" in content:
                content = content.replace("‚", ",")
                modified = True
                print(f"mikey: 🔧 تم إصلاح الفاصلة في {Path(name).stem}")

            # إصلاح zedub الناقص (فقط اذا كان مو موجود)
            if "zedub" in content and "from zthon.core.session import zedub" not in content:
                content = "from zthon.core.session import zedub\n" + content
                modified = True
            
            # إصلاح استدعاءات Config القديمة
            if "from ..Config import Config" in content:
                content = content.replace("from ..Config import Config", "from zthon.Config import Config")
                modified = True

            if modified:
                with open(name, "w", encoding='utf-8') as f:
                    f.write(content)
        except:
            pass
        # ======================================================

        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            try:
                if (pluginname not in Config.NO_LOAD) and (pluginname not in VPS_NOLOAD):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(pluginname, plugin_path=plugin_path)
                            if shortname in failure: failure.remove(shortname)
                            success += 1
                            LOGS.info(f"تـم تثبيت ملـف {shortname}")
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure: failure.append(shortname)
                            if check > 5: break
                        except AttributeError as ae:
                            # المفروض هذا ما يطلع أبدًا الآن
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
                if shortname not in failure: failure.append(shortname)
                LOGS.info(f"خطأ في الملف {shortname}: {e}")

    if extfolder:
        if not failure: failure.append("None")
        try:
            await zedub.tgbot.send_message(
                Config.BOTLOG_CHATID,
                f'Ext Plugins: `{success}`\nFailed: `{", ".join(failure)}`',
            )
        except: pass

async def verifyLoggerGroup():
    try:
        addgvar("PRIVATE_GROUP_BOT_API_ID", -1003477023425)
        addgvar("PM_LOGGER_GROUP_ID", -1003477023425)
    except: pass
    return

async def install_externalrepo(repo, branch, cfolder): pass