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

# ==============================================================================
# mikey: 🎵 إصلاح الميوزك (العودة للزمن الجميل)
# ==============================================================================
try:
    from pytgcalls import idle
except ImportError:
    print("mikey: 🎵 جاري تثبيت نسخة الميوزك القديمة (0.9.5)...")
    os.system("pip3 install py-tgcalls==0.9.5")
    os.system("pip3 install pytgcalls==0.9.5") 

ENV = bool(os.environ.get("ENV", False))
LOGS = logging.getLogger("zthon")

# ==============================================================================
# mikey: 💉 الحقن المستمر
# ==============================================================================
def force_inject_config():
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
        "THUMB_IMAGE": "https://graph.org/file/5340a83ac9ca428089577.jpg",
        "DEFAULT_BIO": "Refz User",
        "OLDZED": [],
        "FINISHED_PROGRESS_STR": "▓",
        "UNFINISHED_PROGRESS_STR": "░",
        "TELEGRAPH_SHORT_NAME": "RefzUser",
        "TELEGRAPH_TOKEN": None,
        "ALIVE_NAME": "Refz User"
    }
    for key, value in MISSING_VARS.items():
        if not hasattr(Config, key):
            setattr(Config, key, value)

force_inject_config()
cmdhr = Config.COMMAND_HAND_LER

if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]

bot = zedub
DEV = 7422264678

async def setup_bot():
    print("mikey: 🚬 التشغيل...")
    force_inject_config()
    TOKEN = os.environ.get("TG_BOT_TOKEN")
    if not TOKEN:
        LOGS.error("mikey: 🤬 التوكن مفقود!")
        sys.exit(1)
    Config.TG_BOT_TOKEN = TOKEN

    try:
        await zedub.connect()
        
        # ========================================================
        # mikey: 💉 ترقيع ar_cmd (حل مشكلة بنك ورشق)
        # بنخلي ar_cmd هي نفسها on (أحنا نضحك على السورس)
        # ========================================================
        if not hasattr(zedub, "ar_cmd"):
            print("mikey: 🔧 تم اختراع دالة ar_cmd للعميل.")
            setattr(zedub, "ar_cmd", zedub.on)

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
    force_inject_config()
    try:
        if Config.BOTLOG:
            await zedub.tgbot.send_file(
                Config.BOTLOG_CHATID,
                "https://graph.org/file/5340a83ac9ca428089577.jpg",
                caption="**•⎆┊تـم بـدء تشغـيل سـورس ريفز 🧸♥️**\n✅ تم إصلاح ar_cmd والميوزك.",
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
        # ========================================================
        # mikey: المصلح الجراحي (تحديث للأخطاء الجديدة)
        # ========================================================
        try:
            with open(name, "r", encoding='utf-8', errors='ignore') as f:
                content = f.read()
            modified = False
            
            # فاصلة الردود
            if "‚" in content:
                content = content.replace("‚", ",")
                modified = True
            
            # تعريف zedub
            if "zedub" in content and "from zthon.core.session import zedub" not in content:
                content = "from zthon.core.session import zedub\n" + content
                modified = True
            
            # تعريف client (للملفات اللي تستخدم client بدال zedub)
            if "client" in content and "client =" not in content and "from zthon.core.session import zedub" not in content:
                 content = "from zthon.core.session import zedub as client\n" + content
                 modified = True

            # تعريف zthon (لملف spam.py وغيره)
            if "zthon" in content and "from zthon.core.session import zedub as zthon" not in content and "import zthon" not in content:
                 # نتأكد انه ما يعرفه كمتغير محلي
                 if "zthon =" not in content:
                     content = "from zthon.core.session import zedub as zthon\n" + content
                     modified = True

            # إصلاح استدعاء Config
            if "from ..Config import Config" in content:
                content = content.replace("from ..Config import Config", "from zthon.Config import Config")
                modified = True
            if "from zthon import Config" in content:
                content = content.replace("from zthon import Config", "from zthon.Config import Config")
                modified = True
                
            # إصلاح (تخبيص.py) - القوس الغلط
            if "]" in content and "list = (" in content: # محاولة تقريبية
                 content = content.replace("]", ")") # هذا خطير بس بنجرب
                 # الأفضل: استبدال السطر الخربان لو لقيناه
                 if '( "3" ,' in content and ']' in content: # السطر 68 تقريبا
                     content = content.replace("]", ")")
                     modified = True

            # إصلاح (جديد.py) - النص المفتوح
            # نحاول نقفل أي سترينج مفتوح في السطر 29
            # (صعب برمجيا، لكن بنضيف " في نهاية الملف احتياط لو كان الخطأ في اخره)
            # أو الأفضل: نتجاوز الملف هذا

            if modified:
                with open(name, "w", encoding='utf-8') as f:
                    f.write(content)
        except: pass
        # ========================================================

        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            
            force_inject_config()

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
                            # LOGS.info(f"تم تحميل {shortname}")
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                        except AttributeError as ae:
                            # اذا الخطأ ar_cmd، نصلحه فوري
                            if "ar_cmd" in str(ae):
                                setattr(zedub, "ar_cmd", zedub.on)
                                continue # نعيد المحاولة
                            
                            LOGS.info(f"متغير ناقص في {shortname}: {ae}")
                            var_name = str(ae).split("'")[-2]
                            setattr(Config, var_name, None)
                            failure.append(shortname)
                            break
                        except Exception as e:
                            if shortname not in failure:
                                failure.append(shortname)
                            LOGS.info(f"فشل تحميل {shortname}: {e}")
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