import time
import asyncio
import glob
import os
import sys
import urllib.request
from datetime import timedelta
from pathlib import Path
import requests
import types

# ==============================================================================
# mikey: 💉 الحقن الشامل (The Ultimate Injection)
# ==============================================================================
print("mikey: ☠️ جاري حقن المطبخ الكامل (Config) لإسكات الملحقات الجائعة...")

# 1. بياناتك
MY_TOKEN = "8297284147:AAHDKI3ncuBhkNq6vLosVujwge5-0Jz8p1A"
# ملاحظة: الآيدي هنا لازم يكون رقم صحيح (Integer) مع السالب
MY_CHANNEL_ID = -1003477023425

# 2. الكلاس المزور (Full Option)
class MikeyConfig:
    # --- الأساسيات ---
    TG_BOT_TOKEN = MY_TOKEN
    APP_ID = 12345678
    API_HASH = "0123456789abcdef0123456789abcdef"
    
    # --- القنوات ---
    PRIVATE_GROUP_ID = MY_CHANNEL_ID
    PRIVATE_GROUP_BOT_API_ID = MY_CHANNEL_ID
    BOTLOG = True
    BOTLOG_CHATID = MY_CHANNEL_ID
    PM_LOGGER_GROUP_ID = MY_CHANNEL_ID
    
    # --- اليوزرات ---
    BOT_USERNAME = "Reevs_Bot"
    TG_BOT_USERNAME = "Reevs_Bot" # حل مشكلة botcontrols
    
    # --- المجلدات (حل مشكلة TMP_DOWNLOAD_DIRECTORY) ---
    TMP_DOWNLOAD_DIRECTORY = "./downloads/"
    TEMP_DIR = "./downloads/"
    
    # --- الأوامر (حل مشكلة SUDO_COMMAND_HAND_LER) ---
    COMMAND_HAND_LER = r"\."
    SUDO_COMMAND_HAND_LER = r"\."
    SUDO_USERS = [] 
    OWNER_ID = 7422264678
    
    # --- متغيرات تعبئة فراغ (عشان الملحقات ما تصيح) ---
    ALIVE_NAME = "Refz User"
    MAX_MESSAGE_SIZE_LIMIT = 4096
    UB_BLACK_LIST_CHAT = []
    NO_LOAD = []
    
    # مفاتيح API وهمية لبعض الملحقات
    DEEP_AI = None
    OCR_SPACE_API_KEY = None
    REM_BG_API_KEY = None
    CHROME_DRIVER = None
    GOOGLE_CHROME_BIN = None
    OPENAI_API_KEY = None
    WEATHER_API = None
    VIRUS_API_KEY = None
    
    # الشعار
    ZEDUBLOGO = None

# 3. إنشاء المجلدات الضرورية
if not os.path.exists("./downloads/"):
    os.makedirs("./downloads/")

# 4. عملية السطو على الذاكرة (Memory Patching)
fake_module = types.ModuleType("Config")
fake_module.Config = MikeyConfig

# نحقن في كل زاوية ممكنة
sys.modules["zthon.Config"] = fake_module
sys.modules["zthon.configs"] = fake_module
sys.modules["Config"] = fake_module

# زرع القيم في البيئة
os.environ["TG_BOT_TOKEN"] = MikeyConfig.TG_BOT_TOKEN
os.environ["PRIVATE_GROUP_ID"] = str(MikeyConfig.PRIVATE_GROUP_ID)
os.environ["TMP_DOWNLOAD_DIRECTORY"] = MikeyConfig.TMP_DOWNLOAD_DIRECTORY
os.environ["SUDO_COMMAND_HAND_LER"] = MikeyConfig.SUDO_COMMAND_HAND_LER

print("mikey: ✅ تم تجهيز الكونفيج.")
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
cmdhr = MikeyConfig.COMMAND_HAND_LER 

if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]

bot = zedub
DEV = 7422264678


async def setup_bot():
    print(f"mikey: 💉 البوت جاهز. القناة المستهدفة: {MikeyConfig.PRIVATE_GROUP_ID}")
    return

async def startupmessage():
    """
    Start up message - الذكية (تحاول القناة، ثم الرسائل المحفوظة)
    """
    try:
        # 1. محاولة الإرسال للقناة
        target_chat = MikeyConfig.BOTLOG_CHATID
        sent = False
        
        if MikeyConfig.BOTLOG:
            try:
                # محاولة الإرسال المباشر
                MikeyConfig.ZEDUBLOGO = await zedub.tgbot.send_file(
                    target_chat,
                    "https://graph.org/file/5340a83ac9ca428089577.jpg",
                    caption="**•⎆┊تـم بـدء تشغـيل سـورس ريفز (Mikey Final Fix) 🧸♥️**\n\n✅ الملحقات تعمل.\n✅ التوكن محقون.",
                    buttons=[(Button.url("𝗦َِ𝗼َِ𝗨َِ𝗿َِ𝗖َِ𝗲 َِ𝗥َِ𝗲َِ𝗙َِ𝘇", "https://t.me/def_Zoka"),)],
                )
                sent = True
            except Exception as e:
                print(f"mikey: تعذر الإرسال للقناة ({e})... جاري التحويل للرسائل المحفوظة.")

        # 2. الخطة البديلة: الرسائل المحفوظة (me)
        if not sent:
            try:
                await zedub.tgbot.send_message(
                    "me",
                    "**🚨 تنبيه من مايكي:**\nالبوت شغال والملحقات تحملت، بس مو قادر يوصل لقناة اللوج (يمكن لأنك مو ضايف البوت فيها أو الآيدي غلط).\n\nالمهم: **أنا حي!** 🚬"
                )
                print("mikey: ✅ تم إرسال رسالة التنبيه للرسائل المحفوظة.")
            except Exception as e2:
                print(f"mikey: حتى الرسائل المحفوظة فشلت! {e2}")

    except Exception as e:
        LOGS.error(e)
        return None
    
    # تحديثات الريستارت
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
            await zedub.check_testcases()
            message = await zedub.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n**•⎆┊تـم إعـادة تشغيـل السـورس بنجــاح 🧸♥️**"
            await zedub.edit_message(msg_details[0], msg_details[1], text)
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


async def mybot():
    print("mikey: 🛑 mybot skipped.")
    return

async def add_bot_to_logger_group(chat_id):
    pass

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
                # نستخدم MikeyConfig
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
                            # فلترة الأخطاء عشان نعرف الناقص
                            print(f"mikey: ⚠️ الملحق {shortname} يبي متغير: {ae}")
                            failure.append(shortname)
                            break
                        except Exception as e:
                            # اخطاء أخرى (syntax error في الملحق نفسه مثلا)
                            # print(f"mikey: خطأ في الملحق {shortname}: {e}") 
                            failure.append(shortname)
                            break
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)

    if extfolder:
        if not failure:
            failure.append("None")
        try:
            # نحاول نرسل للقناة او المحفوظات
            dest = MikeyConfig.BOTLOG_CHATID
            await zedub.tgbot.send_message(
                dest,
                f'Ext Plugins: `{success}`\nFailed: `{", ".join(failure)}`',
            )
        except:
            pass

async def verifyLoggerGroup():
    print("mikey: 🛑 verifyLoggerGroup bypassed.")
    return

async def install_externalrepo(repo, branch, cfolder):
    pass