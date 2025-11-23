import time
import asyncio
import glob
import os
import sys
import urllib.request
from datetime import timedelta
from pathlib import Path
import requests

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

# ==============================================================================
# mikey: منطقة الفرض الجبري (Mikey's Hardcoded Config v2) 💉
# ==============================================================================
print("mikey: ☠️ جاري تفعيل الملف المعدل (الإصدار الكامل)...")

# 1. بياناتك
MY_TOKEN = "8297284147:AAHDKI3ncuBhkNq6vLosVujwge5-0Jz8p1A"
MY_CHANNEL = -1003477023425

# 2. زرع القيم في النظام
os.environ["TG_BOT_TOKEN"] = MY_TOKEN
os.environ["PRIVATE_GROUP_ID"] = str(MY_CHANNEL)
os.environ["PRIVATE_GROUP_BOT_API_ID"] = str(MY_CHANNEL)
os.environ["BOT_USERNAME"] = "Reevs_Bot"
os.environ["BOTLOG"] = "True"
os.environ["BOTLOG_CHATID"] = str(MY_CHANNEL)
os.environ["PM_LOGGER_GROUP_ID"] = str(MY_CHANNEL)

# 3. المتغيرات العامة
BOTLOG = True
BOTLOG_CHATID = MY_CHANNEL
PM_LOGGER_GROUP_ID = MY_CHANNEL

# 4. كلاس Config المزيف (تمت توسعته ليشمل طلبات الملحقات)
class Config:
    # الأساسيات
    TG_BOT_TOKEN = MY_TOKEN
    BOT_USERNAME = "Reevs_Bot"
    PRIVATE_GROUP_ID = MY_CHANNEL
    PRIVATE_GROUP_BOT_API_ID = MY_CHANNEL
    BOTLOG = True
    BOTLOG_CHATID = MY_CHANNEL
    PM_LOGGER_GROUP_ID = MY_CHANNEL
    
    # الأوامر والبادئات (عشان الملحقات تشتغل)
    COMMAND_HAND_LER = r"\."
    SUDO_COMMAND_HAND_LER = r"\."
    TMP_DOWNLOAD_DIRECTORY = "./downloads/"
    TEMP_DIR = "./downloads/"
    
    # قوائم التحميل
    NO_LOAD = []
    
    # أي شي ثاني ممكن يطلبونه
    ALIVE_NAME = "My Userbot"
    MAX_MESSAGE_SIZE_LIMIT = 4096
    ZEDUBLOGO = None 

# 5. إنشاء مجلد التحميل عشان ما يكرش
if not os.path.exists(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)

# ==============================================================================

ENV = bool(os.environ.get("ENV", False))
LOGS = logging.getLogger("zthon")
cmdhr = Config.COMMAND_HAND_LER

if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]

bot = zedub
DEV = 7422264678

async def setup_bot():
    """
    mikey: دالة الحقن المباشر
    """
    print(f"mikey: 💉 تم تثبيت التوكن والقناة: {MY_CHANNEL}")
    
    # محاولة للحقن في الكلاس الاصلي لو انوجد
    try:
        import zthon.configs as real_config
        real_config.Config.TG_BOT_TOKEN = MY_TOKEN
        real_config.Config.PRIVATE_GROUP_ID = MY_CHANNEL
        real_config.Config.TMP_DOWNLOAD_DIRECTORY = "./downloads/"
        real_config.Config.SUDO_COMMAND_HAND_LER = r"\."
    except:
        pass
        
    return

async def startupmessage():
    """
    Start up message
    """
    try:
        if BOTLOG:
            try:
                Config.ZEDUBLOGO = await zedub.tgbot.send_file(
                    BOTLOG_CHATID,
                    "https://graph.org/file/5340a83ac9ca428089577.jpg",
                    caption="**•⎆┊تـم بـدء تشغـيل سـورس ريفز المعدل (Mikey Edition) 🧸♥️**",
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
                if (pluginname not in Config.NO_LOAD) and (
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
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                # mikey: لا تحذف شي، بس سجل الخطأ
                LOGS.info(
                    f"لا يمكنني تحميل {shortname} بسبب الخطأ {e}"
                )
    if extfolder:
        if not failure:
            failure.append("None")
        await zedub.tgbot.send_message(
            BOTLOG_CHATID,
            f'Ext Plugins: `{success}`\nFailed: `{", ".join(failure)}`',
        )

async def verifyLoggerGroup():
    print("mikey: 🛑 verifyLoggerGroup bypassed.")
    return

async def install_externalrepo(repo, branch, cfolder):
    # mikey: تجاوزت هذا الجزء لأنه غير مهم حاليا
    pass 