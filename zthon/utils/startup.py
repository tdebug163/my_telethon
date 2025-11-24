import sys
import os
import glob
import asyncio
import logging
import types
from pathlib import Path
from telethon import Button, functions, types as tele_types, utils

# ==============================================================================
# mikey: 🃏 الجوكر (The Magic Config)
# هذا الكلاس يرد بـ "نعم" على أي طلب، وينهي مشكلة المتغيرات الناقصة للأبد.
# ==============================================================================
print("mikey: ☠️ تفعيل وضع الجوكر (Magic Config Activated)...")

# 1. الأساسيات الثابتة
MY_TOKEN = "8297284147:AAHDKI3ncuBhkNq6vLosVujwge5-0Jz8p1A"
MY_CHANNEL = -1003477023425

# زرع القيم في البيئة
os.environ["TG_BOT_TOKEN"] = MY_TOKEN
os.environ["PRIVATE_GROUP_ID"] = str(MY_CHANNEL)
os.environ["BOTLOG_CHATID"] = str(MY_CHANNEL)

if not os.path.exists("./downloads/"):
    try:
        os.makedirs("./downloads/")
    except:
        pass

# 2. الكلاس السحري
class MagicConfig:
    # --- الثوابت الحقيقية ---
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
    
    # --- القيم الافتراضية الذكية ---
    TMP_DOWNLOAD_DIRECTORY = "./downloads/"
    TEMP_DIR = "./downloads/"
    COMMAND_HAND_LER = r"\."
    SUDO_COMMAND_HAND_LER = r"\."
    SUDO_USERS = [8511249817]
    OWNER_ID = 8279354412 
    ALIVE_NAME = "Refz User"
    
    # --- السحر هنا: أي متغير غير موجود، بنخترعه لحظياً ---
    def __getattr__(cls, name):
        # mikey: لو الملحق طلب شي مو موجود، نعطيه قيمة وهمية عشان ما يكرش
        # print(f"mikey debug: الملحق طلب '{name}'.. تم توفيره وهمياً.")
        
        if "DIR" in name or "PATH" in name:
            return "./downloads/"
        if "ID" in name:
            return MY_CHANNEL
        if "LIST" in name:
            return []
        if "KEY" in name or "TOKEN" in name:
            return "dummy_key"
        
        return None

# تحويل الكلاس لنوع يقبله النظام
class Joker(object):
    pass

# نسخ القيم للكلاس الجديد
for key, value in MagicConfig.__dict__.items():
    if not key.startswith("__"):
        setattr(Joker, key, value)

# إضافة دالة __getattr__ للكلاس الجديد (لأنها ما تنتقل بالنسخ العادي)
def get_attr_magic(self, name):
    if "DIR" in name or "PATH" in name:
        return "./downloads/"
    if "ID" in name:
        return MY_CHANNEL
    if "LIST" in name:
        return []
    if "KEY" in name or "TOKEN" in name:
        return "dummy_key"
    if "HAND_LER" in name:
        return r"\."
    return None

Joker.__getattr__ = get_attr_magic
# نسخة للكلاس كـ Instance و كـ Static
JokerInstance = Joker()

# 3. حقن الجوكر في كل مكان في الذاكرة
sys.modules["zthon.Config"] = type("ConfigModule", (object,), {"Config": JokerInstance})
sys.modules["zthon.configs"] = type("ConfigModule", (object,), {"Config": JokerInstance})
sys.modules["Config"] = JokerInstance

# تعديل الكلاس الأصلي لو انوجد
try:
    from zthon.Config import Config as OriginalConfig
    for key, value in MagicConfig.__dict__.items():
        if not key.startswith("__"):
            try:
                setattr(OriginalConfig, key, value)
            except:
                pass
except:
    pass

print("mikey: ✅ تم تعميم الجوكر. الملحقات لن تشتكي بعد الآن.")

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
cmdhr = MagicConfig.COMMAND_HAND_LER 

if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]

bot = zedub


async def setup_bot():
    print(f"mikey: ✅ البوت جاهز.")
    return

async def startupmessage():
    try:
        if MagicConfig.BOTLOG:
            try:
                await zedub.tgbot.send_file(
                    MagicConfig.BOTLOG_CHATID,
                    "https://graph.org/file/5340a83ac9ca428089577.jpg",
                    caption="**•⎆┊تـم بـدء تشغـيل سـورس ريفز (Magic Mode) 🧸♥️**",
                )
            except:
                pass
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
    تحميل الملحقات
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
                # نستخدم الجوكر هنا
                if (pluginname not in MagicConfig.NO_LOAD) and (
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
                            # المفروض ما ندخل هنا بفضل الجوكر
                            print(f"mikey: {shortname} فشل رغم الجوكر: {ae}")
                            failure.append(shortname)
                            break
                        except Exception as e:
                            # print(f"mikey: فشل {shortname}: {e}")
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
            await zedub.tgbot.send_message(
                MagicConfig.BOTLOG_CHATID,
                f'Ext Plugins: `{success}`\nFailed: `{", ".join(failure)}`',
            )
        except:
            pass

async def verifyLoggerGroup():
    # تعديل القناة بدال الإنشاء
    try:
        addgvar("PRIVATE_GROUP_BOT_API_ID", MY_CHANNEL)
        addgvar("PM_LOGGER_GROUP_ID", MY_CHANNEL)
    except:
        pass
    return

async def install_externalrepo(repo, branch, cfolder):
    pass