import time
import asyncio
import glob
import os
import sys
import urllib.request
from datetime import timedelta
from pathlib import Path
import requests

# ==============================================================================
# mikey: 💉 عملية السطو المسلح على الذاكرة (Memory Hijack)
# هذا الكود لازم يكون في البداية عشان يخدع الملحقات
# ==============================================================================
print("mikey: ☠️ جاري حقن الكونفيج في ذاكرة النظام (sys.modules)...")

# 1. تعريف الكلاس المزيف الشامل (يحوي كل طلبات الملحقات)
class MikeyConfig:
    # الأساسيات
    TG_BOT_TOKEN = "8297284147:AAHDKI3ncuBhkNq6vLosVujwge5-0Jz8p1A"
    PRIVATE_GROUP_ID = -1003477023425
    PRIVATE_GROUP_BOT_API_ID = -1003477023425
    BOT_USERNAME = "Reevs_Bot"
    BOTLOG = True
    BOTLOG_CHATID = -1003477023425
    PM_LOGGER_GROUP_ID = -1003477023425
    
    # طلبات الملحقات (اللي كانت تطلع احمر)
    TMP_DOWNLOAD_DIRECTORY = "./downloads/"
    TEMP_DIR = "./downloads/"
    COMMAND_HAND_LER = r"\."
    SUDO_COMMAND_HAND_LER = r"\."
    SUDO_USERS = [] # قائمة المطورين
    OWNER_ID = 7422264678 # حط ايديك هنا لو تبي
    
    # متغيرات اضافية عشان نسكت الباقين
    ALIVE_NAME = "Refz User"
    MAX_MESSAGE_SIZE_LIMIT = 4096
    UB_BLACK_LIST_CHAT = []
    NO_LOAD = []
    DEEP_AI = None
    OCR_SPACE_API_KEY = None
    REM_BG_API_KEY = None
    CHROME_DRIVER = None
    GOOGLE_CHROME_BIN = None
    OPENAI_API_KEY = None
    
    # شعار وهمي
    ZEDUBLOGO = None

# 2. إنشاء مجلد التحميل
if not os.path.exists("./downloads/"):
    os.makedirs("./downloads/")

# 3. حقن الكلاس في كل المسارات المحتملة (عشان الملحقات تشوفه)
import types
fake_module = types.ModuleType("Config")
fake_module.Config = MikeyConfig

sys.modules["zthon.Config"] = fake_module
sys.modules["zthon.configs"] = fake_module
sys.modules["Config"] = fake_module

# زرع القيم في البيئة
os.environ["TG_BOT_TOKEN"] = MikeyConfig.TG_BOT_TOKEN
os.environ["PRIVATE_GROUP_ID"] = str(MikeyConfig.PRIVATE_GROUP_ID)
os.environ["TMP_DOWNLOAD_DIRECTORY"] = MikeyConfig.TMP_DOWNLOAD_DIRECTORY

print("mikey: ✅ تم الحقن. الملحقات الآن تحت السيطرة.")
# ==============================================================================

from telethon import Button, functions, types, utils
from telethon.tl.functions.channels import JoinChannelRequest

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
from .tools import create_supergroup


ENV = bool(os.environ.get("ENV", False))
LOGS = logging.getLogger("zthon")
# نستخدم الكلاس المحقون
cmdhr = MikeyConfig.COMMAND_HAND_LER 

if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]

bot = zedub
DEV = 7422264678


async def setup_bot():
    """
    mikey: دالة الحقن المباشر (تأكيد)
    """
    print(f"mikey: 💉 النظام يعمل ببيانات القناة: {MikeyConfig.PRIVATE_GROUP_ID}")
    return

async def startupmessage():
    """
    Start up message
    """
    try:
        if MikeyConfig.BOTLOG:
            try:
                MikeyConfig.ZEDUBLOGO = await zedub.tgbot.send_file(
                    MikeyConfig.BOTLOG_CHATID,
                    "https://graph.org/file/5340a83ac9ca428089577.jpg",
                    caption="**•⎆┊تـم بـدء تشغـيل سـورس ريفز (Mikey Hacked Version) 🧸♥️**",
                    buttons=[(Button.url("𝗦َِ𝗼َِ𝗨َِ𝗿َِ𝗖َِ𝗲 َِ𝗥َِ𝗲َِ𝗙َِ𝘇", "https://t.me/def_Zoka"),)],
                )
            except Exception as e:
                print(f"mikey: فشل ارسال رسالة البدء (عادي): {e}")

    except Exception as e:
        LOGS.error(e)
        return None
    
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await zedub.check_testcases()
            message = await zedub.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n**•⎆┊تـم إعـادة تشغيـل السـورس بنجــاح 🧸♥️**"
            await zedub.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
                await zedub.send_message(
                    msg_details[0],
                    f"{cmdhr}بنك",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


async def mybot():
    print("mikey: 🛑 mybot skipped.")
    return

async def add_bot_to_logger_group(chat_id):
    try:
        bot_details = await zedub.tgbot.get_me()
        await zedub(
            functions.messages.AddChatUserRequest(
                chat_id=chat_id,
                user_id=bot_details.username,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            bot_details = await zedub.tgbot.get_me()
            await zedub(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id,
                    users=[bot_details.username],
                )
            )
        except Exception as e:
            LOGS.error(str(e))


zthon = {"@def_Zoka", "@refz_var", "@KALAYISH", "@senzir2", "rev_fxx"}

async def saves():
    print("mikey: 🛑 saves skipped.")
    return


async def load_plugins(folder, extfolder=None):
    """
    To load plugins
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
                # نستخدم MikeyConfig هنا
                if (pluginname not in MikeyConfig.NO_LOAD) and (
                    pluginname not in VPS_NOLOAD
                ):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(
                                pluginname,
                                plugin_path=plugin_path,
                            )
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
                             # mikey: هذا عشان نصيد اي متغير ناقص ونضيفه
                            print(f"mikey: الملحق {shortname} يبي متغير ناقص: {ae}")
                            failure.append(shortname)
                            break
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                # mikey: سجل الخطأ بس
                LOGS.info(
                    f"لا يمكنني تحميل {shortname} بسبب الخطأ {e}"
                )
    if extfolder:
        if not failure:
            failure.append("None")
        await zedub.tgbot.send_message(
            MikeyConfig.BOTLOG_CHATID,
            f'Ext Plugins: `{success}`\nFailed: `{", ".join(failure)}`',
        )

async def verifyLoggerGroup():
    print("mikey: 🛑 verifyLoggerGroup bypassed.")
    return

async def install_externalrepo(repo, branch, cfolder):
    pass