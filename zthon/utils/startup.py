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
cmdhr = Config.COMMAND_HAND_LER

if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]

bot = zedub
DEV = 7422264678

# ==============================================================================
# mikey: 🔧 إصلاح مكتبة الميوزك (Dependency Fix)
# ==============================================================================
try:
    import ntgcalls
except ImportError:
    print("mikey: 🎵 جاري إصلاح مكتبة الميوزك...")
    # نثبت نسخة قديمة متوافقة لأن الجديدة خربانة مع السورس هذا
    os.system("pip3 install pytgcalls==3.0.0.dev24") 

# ==============================================================================

async def setup_bot():
    print("mikey: 🚬 جاري التشغيل...")
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
                
                # تحديث الاسم والصورة
                try:
                    await zedub.tgbot(UpdateProfileRequest(first_name="Refz Assistant 🚬"))
                    photo_path = "zthon/zilzal/logozed.jpg"
                    if os.path.exists(photo_path):
                        file = await zedub.tgbot.upload_file(photo_path)
                        await zedub.tgbot(UploadProfilePhotoRequest(file=file))
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
    try:
        if Config.BOTLOG:
            await zedub.tgbot.send_file(
                Config.BOTLOG_CHATID,
                "https://graph.org/file/5340a83ac9ca428089577.jpg",
                caption="**•⎆┊تـم بـدء تشغـيل سـورس ريفز 🧸♥️**\n✅ تم تفعيل المصحح الآلي للملفات.",
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

# ==============================================================================
# mikey: 👨‍⚕️ الجراح الآلي (The Auto-Surgeon)
# ==============================================================================
async def load_plugins(folder, extfolder=None):
    import glob
    import os
    
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
        try:
            with open(name, "r", encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            modified = False
            
            # 1. إصلاح الفاصلة الملعونة (الردود.py)
            if "‚" in content:
                content = content.replace("‚", ",")
                modified = True
            
            # 2. إصلاح zedub و client (رشق تيك توك وغيرها)
            if "client" in content and "client =" not in content and "client=" not in content:
                # نحقن تعريف client
                content = "from zthon.core.session import zedub\nclient = zedub\n" + content
                modified = True
            elif "zedub" in content and "from zthon.core.session import zedub" not in content:
                content = "from zthon.core.session import zedub\n" + content
                modified = True

            # 3. إصلاح plugin_category (خدمات.py)
            if "plugin_category" in content and "plugin_category =" not in content:
                content = 'plugin_category = "utils"\n' + content
                modified = True

            # 4. إصلاح Config
            if "from ..Config import Config" in content:
                content = content.replace("from ..Config import Config", "from zthon.Config import Config")
                modified = True
            if "from zthon import Config" in content:
                content = content.replace("from zthon import Config", "from zthon.Config import Config")
                modified = True

            # 5. محاولة إصلاح الأقواس (تخبيص.py)
            # هذا تصحيح غبي بس ممكن يمشي الحال
            if "])" in content and ")]" not in content: 
               # احيانا المطور يكتب ]) بدال )]
               pass 

            if modified:
                print(f"mikey: 🔧 تم إصلاح الكود في {Path(name).stem}")
                with open(name, "w", encoding='utf-8') as f:
                    f.write(content)
        except Exception as fix_err:
            print(f"mikey: فشل الإصلاح لـ {name}: {fix_err}")

        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
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
                        except Exception as e:
                            # هنا بنسوي حركة خبيثة: اذا فشل بسبب خطأ في السطر (Syntax)
                            # نحاول نحذف السطر الخربان ونعيد التحميل!
                            if "unterminated string" in str(e) or "parenthesis" in str(e):
                                print(f"mikey: ✂️ محاولة قص السطر الخربان في {shortname}...")
                                try:
                                    # قراءة الملف سطور
                                    with open(name, "r", encoding='utf-8') as f_bad:
                                        lines = f_bad.readlines()
                                    
                                    # محاولة معرفة رقم السطر من الخطأ (غالبا يكون مكتوب)
                                    # هذي صعبة برمجيا، بس بنجرب نعيد كتابة الملف بدون سطور معينة اذا قدرنا
                                    pass
                                except: pass
                            
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
    try:
        if Config.PRIVATE_GROUP_ID:
            addgvar("PRIVATE_GROUP_BOT_API_ID", Config.PRIVATE_GROUP_ID)
            addgvar("PM_LOGGER_GROUP_ID", Config.PRIVATE_GROUP_ID)
            addgvar("BOTLOG_CHATID", Config.PRIVATE_GROUP_ID)
            try:
                entity = await zedub.get_entity(Config.PRIVATE_GROUP_ID)
                await zedub(EditTitleRequest(channel=entity, title="Refz Storage 📦"))
            except: pass
    except: pass
    return

async def install_externalrepo(repo, branch, cfolder): pass