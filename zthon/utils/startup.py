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

async def setup_bot():
    print("mikey: 🚬 التشغيل...")
    # نعتمد على Config اللي عبيناه
    try:
        await zedub.connect()
        if Config.TG_BOT_TOKEN:
            try:
                await zedub.tgbot.start(bot_token=Config.TG_BOT_TOKEN)
                bot_details = await zedub.tgbot.get_me()
                Config.TG_BOT_USERNAME = f"@{bot_details.username}"
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
        sys.exit(1)

async def startupmessage():
    try:
        if Config.BOTLOG:
            await zedub.tgbot.send_file(
                Config.BOTLOG_CHATID,
                "https://graph.org/file/5340a83ac9ca428089577.jpg",
                caption="**•⎆┊تـم بـدء تشغـيل سـورس ريفز 🧸♥️**\n✅ تم حقن NO_LOAD بنجاح.",
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
    
    # ==============================================================================
    # mikey: 💉 الحقنة القاتلة للخطأ (NO_LOAD Injection)
    # ==============================================================================
    # نتأكد إن المتغير موجود قبل ما نبدأ أي شي
    if not hasattr(Config, "NO_LOAD"):
        print("mikey: ⚠️ تم اكتشاف غياب NO_LOAD.. جاري الحقن.")
        Config.NO_LOAD = []
        
    # ونحقن الباقين احتياط عشان ما يرجع يبكي
    if not hasattr(Config, "TMP_DOWNLOAD_DIRECTORY"): Config.TMP_DOWNLOAD_DIRECTORY = "./downloads/"
    if not hasattr(Config, "SUDO_COMMAND_HAND_LER"): Config.SUDO_COMMAND_HAND_LER = r"\."
    # ==============================================================================

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
        # المصلح الآلي
        try:
            with open(name, "r", encoding='utf-8', errors='ignore') as f:
                content = f.read()
            modified = False
            if "‚" in content:
                content = content.replace("‚", ",")
                modified = True
            if "zedub" in content and "from zthon.core.session import zedub" not in content:
                content = "from zthon.core.session import zedub\n" + content
                modified = True
            if "from ..Config import Config" in content:
                content = content.replace("from ..Config import Config", "from zthon.Config import Config")
                modified = True
            if modified:
                with open(name, "w", encoding='utf-8') as f:
                    f.write(content)
        except: pass

        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            try:
                # الآن مستحيل يكرش هنا لأننا حقناها فوق
                if (pluginname not in Config.NO_LOAD):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(pluginname, plugin_path=plugin_path)
                            if shortname in failure:
                                failure.remove(shortname)
                            success += 1
                            # LOGS.info(f"تـم تثبيت ملـف {shortname}")
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                        except AttributeError as ae:
                            # لو طلع خطأ هنا، بنعرفه ونحقنه المرة الجاية
                            LOGS.info(f"متغير ناقص في {shortname}: {ae}")
                            failure.append(shortname)
                            break
                        except Exception as e:
                            # نتجاوز الملفات المضروبة برمجياً (Syntax Error)
                            LOGS.info(f"فشل {shortname}: {e}")
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