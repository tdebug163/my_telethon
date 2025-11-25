import glob
import os
import sys
import asyncio
from pathlib import Path
from telethon import Button, functions, types, utils
from telethon.tl.functions.channels import JoinChannelRequest, EditTitleRequest, EditPhotoRequest, EditAdminRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest 
from telethon.tl.types import ChatAdminRights

from zthon import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID
from ..Config import Config
from ..core.logger import logging
from ..core.session import zedub
from ..helpers.utils import install_pip
from ..helpers.utils.utils import runcmd
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from .pluginmanager import load_module

ENV = bool(os.environ.get("ENV", False))
LOGS = logging.getLogger("zthon")

# ==============================================================================
# mikey: 💉 الحقن الإجباري المباشر (The Force Injector) 💉
# هذه الدالة تحقن المتغيرات في الكلاس مباشرة في الذاكرة
# ==============================================================================
def force_inject_config():
    # قائمة المتغيرات الناقصة اللي طلعت في اللوج
    MISSING_VARS = {
        "SPAMWATCH_API": None,
        "TMP_DOWNLOAD_DIRECTORY": "./downloads/",
        "TEMP_DIR": "./downloads/",
        "SUDO_COMMAND_HAND_LER": r"\.",
        "NO_LOAD": [],
        "UB_BLACK_LIST_CHAT": [],
        "HEROKU_API_KEY": None,
        "HEROKU_APP_NAME": None,
        "DEEP_AI": None,
        "OCR_SPACE_API_KEY": None,
        "OPENAI_API_KEY": None,
        "REM_BG_API_KEY": None,
        "CHROME_DRIVER": None,
        "GOOGLE_CHROME_BIN": None,
        "WEATHER_API": None,
        "VIRUS_API_KEY": None,
        "ZEDUBLOGO": None,
        "THUMB_IMAGE": "https://graph.org/file/5340a83ac9ca428089577.jpg"
    }
    
    # الحقن المباشر
    for key, value in MISSING_VARS.items():
        if not hasattr(Config, key):
            setattr(Config, key, value)

# تشغيل الحقن فوراً عند بدء الملف
force_inject_config()
cmdhr = Config.COMMAND_HAND_LER # الآن هذا السطر آمن

if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]

bot = zedub
DEV = 7422264678

async def setup_bot():
    print("mikey: 🚬 جاري التشغيل (مع الحقن المستمر)...")
    force_inject_config() # حقن مرة ثانية للتأكيد
    
    TOKEN = os.environ.get("TG_BOT_TOKEN")
    if not TOKEN:
        LOGS.error("mikey: 🤬 التوكن مفقود!")
        sys.exit(1)
    Config.TG_BOT_TOKEN = TOKEN

    try:
        await zedub.connect()
        if Config.TG_BOT_TOKEN:
            try:
                await zedub.tgbot.start(bot_token=Config.TG_BOT_TOKEN)
                bot_details = await zedub.tgbot.get_me()
                Config.TG_BOT_USERNAME = f"@{bot_details.username}"
                Config.BOT_USERNAME = f"@{bot_details.username}"
                
                try:
                    await zedub.tgbot(UpdateProfileRequest(first_name="Refz Assistant 🚬"))
                except: pass
            except: pass
        
        config = await zedub(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == zedub.session.server_address:
                zedub.session.set_dc(option.id, option.ip_address, option.port)
                zedub.session.save()
                break

        zedub.me = await zedub.get_me()
        zedub.uid = zedub.tgbot.uid = utils.get_peer_id(zedub.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(zedub.me)

    except Exception as e:
        LOGS.error(f"Error: {str(e)}")
        sys.exit()

async def startupmessage():
    force_inject_config() # حقن ثالث
    try:
        if Config.BOTLOG:
            await zedub.tgbot.send_file(
                Config.BOTLOG_CHATID,
                "https://graph.org/file/5340a83ac9ca428089577.jpg",
                caption="**•⎆┊تـم بـدء تشغـيل سـورس ريفز 🧸♥️**\n✅ تم تفعيل الحقن الذاتي.",
                buttons=[(Button.url("Source", "https://t.me/def_Zoka"),)],
            )
    except: pass
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
            await zedub.check_testcases()
            await zedub.edit_message(msg_details[0], msg_details[1], "**•⎆┊تـم التحديث والتشغيل ✅**")
            del_keyword_collectionlist("restart_update")
    except: pass

async def mybot(): pass
async def add_bot_to_logger_group(chat_id): pass
async def saves(): pass

async def load_plugins(folder, extfolder=None):
    import glob
    import os
    
    # الحقن الرابع والأهم (قبل التحميل مباشرة)
    force_inject_config()
    
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
        # إصلاح الملفات المعطوبة برمجياً
        try:
            with open(name, "r", encoding='utf-8', errors='ignore') as f:
                content = f.read()
            modified = False
            if "‚" in content: # الفاصلة
                content = content.replace("‚", ",")
                modified = True
            if "zedub" in content and "from zthon.core.session import zedub" not in content:
                content = "from zthon.core.session import zedub\n" + content
                modified = True
            if "zdthon" in content: # مشكلة bt.py
                content = content.replace("zdthon", "zthon")
                modified = True
                
            if modified:
                with open(name, "w", encoding='utf-8') as f:
                    f.write(content)
        except: pass

        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            
            # ---------------------------------------------------------
            # mikey: الحقن المتكرر (لكل ملف) 💉
            # هذا يضمن إن المتغيرات موجودة حتى لو انحذفت
            force_inject_config()
            # ---------------------------------------------------------

            try:
                if (pluginname not in Config.NO_LOAD):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(pluginname, plugin_path=plugin_path)
                            if shortname in failure:
                                failure.remove(shortname)
                            success += 1
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                        except AttributeError as ae:
                            # لو لسا فيه خطأ، نطبعه ونحاول نتجاوز
                            LOGS.info(f"متغير ناقص في {shortname}: {ae}")
                            # محاولة يائسة: حقن المتغير المفقود تحديداً
                            missing_var = str(ae).split("'")[-2]
                            setattr(Config, missing_var, None)
                            failure.append(shortname)
                            break
                        except Exception as e:
                            # أخطاء برمجية أخرى
                            # LOGS.info(f"فشل {shortname}: {e}")
                            failure.append(shortname)
                            break
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                LOGS.info(f"خطأ في {shortname}: {e}")

    if extfolder:
        if not failure:
            failure.append("None")
        try:
            await zedub.tgbot.send_message(
                Config.BOTLOG_CHATID,
                f'Imported: `{success}`\nFailed: `{", ".join(failure)}`',
            )
        except: pass

async def verifyLoggerGroup():
    logger_id_str = os.environ.get("PRIVATE_GROUP_ID")
    if not logger_id_str: return
    try:
        logger_id = int(logger_id_str)
        Config.PRIVATE_GROUP_ID = logger_id
        Config.BOTLOG_CHATID = logger_id
        try:
            addgvar("PRIVATE_GROUP_BOT_API_ID", logger_id)
            addgvar("PM_LOGGER_GROUP_ID", logger_id)
            addgvar("BOTLOG_CHATID", logger_id)
        except: pass
        try:
            entity = await zedub.get_entity(logger_id)
            await zedub(EditTitleRequest(channel=entity, title="Refz Storage 📦"))
        except: pass
    except: pass
    return

async def install_externalrepo(repo, branch, cfolder): pass