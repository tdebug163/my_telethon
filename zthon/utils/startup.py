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
from telethon.tl.functions.channels import JoinChannelRequest, EditTitleRequest, EditPhotoRequest, EditAdminRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhoto
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

# mikey: ما نحتاج tools.py لأننا ما راح ننشئ شي
# from .tools import create_supergroup 

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
# mikey: دالة الإعداد (Setup) - النسخة الصارمة ☠️
# ==============================================================================
async def setup_bot():
    """
    تجهيز البوت والتأكد من وجود التوكن
    """
    print("mikey: 🚬 جاري فحص التوكن والبيانات من ريندر...")
    
    # 1. سحب التوكن من ريندر مباشرة
    TOKEN = os.environ.get("TG_BOT_TOKEN")
    
    if not TOKEN:
        LOGS.error("mikey: 😡 يا قح** وين التوكن؟ حط TG_BOT_TOKEN في ريندر لا أجي ألعن خيرك!")
        sys.exit(1)
    
    Config.TG_BOT_TOKEN = TOKEN

    try:
        await zedub.connect()
        
        # محاولة تشغيل البوت المساعد
        try:
            await zedub.tgbot.start(bot_token=TOKEN)
            bot_details = await zedub.tgbot.get_me()
            Config.TG_BOT_USERNAME = f"@{bot_details.username}"
            Config.BOT_USERNAME = f"@{bot_details.username}"
            print(f"mikey: ✅ تم تفعيل البوت المساعد: {Config.TG_BOT_USERNAME}")
            
            # محاولة تحديث معلومات البوت (صورة واسم)
            # ملاحظة: البوتات لها قيود في تعديل نفسها عبر API، لكن بنحاول بالمتوفر
            try:
                # نغير الاسم الأول للبوت (تحديث شكلي)
                await zedub.tgbot(UpdateProfileRequest(first_name="Refz Assistant 🚬"))
                print("mikey: ✏️ تم تحديث اسم البوت.")
            except Exception as e:
                print(f"mikey: ما قدرت أغير اسم البوت (عادي): {e}")

        except Exception as e:
            LOGS.error(f"mikey: 😡 التوكن غلط أو البوت مبند! شيك عليه: {e}")
            sys.exit(1)

        # إعدادات السيرفر والاتصال
        config = await zedub(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == zedub.session.server_address:
                if zedub.session.dc_id != option.id:
                    LOGS.warning(f"ايـدي DC ثـابت فـي الجلسـة مـن {zedub.session.dc_id} الـى {option.id}")
                zedub.session.set_dc(option.id, option.ip_address, option.port)
                zedub.session.save()
                break

        zedub.me = await zedub.get_me()
        zedub.uid = zedub.tgbot.uid = utils.get_peer_id(zedub.me)

        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(zedub.me)

    except Exception as e:
        LOGS.error(f"كـود تيرمكس - {str(e)}")
        sys.exit()


async def startupmessage():
    """
    Start up message in telegram logger group
    """
    try:
        if BOTLOG:
            # محاولة إرسال صورة ورسالة
            try:
                Config.ZEDUBLOGO = await zedub.tgbot.send_file(
                    BOTLOG_CHATID,
                    "https://graph.org/file/5340a83ac9ca428089577.jpg",
                    caption="**•⎆┊تـم بـدء تشغـيل سـورس ريفز (Mikey Fixed Edition) 🧸♥️**",
                    buttons=[(Button.url("𝗦َِ𝗼َِ𝗨َِ𝗿َِ𝗖َِ𝗲 َِ𝗥َِ𝗲َِ𝗙َِ𝘇", "https://t.me/def_Zoka"),)],
                )
            except Exception as e:
                LOGS.warning(f"mikey: ما قدرت أرسل لقناة اللوج (تأكد البوت مشرف): {e}")

    except Exception as e:
        LOGS.error(e)
        return None

    # كود التحديث (Restore)
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


# ==============================================================================
# mikey: تم إعدام دالة mybot القديمة اللي تكلم BotFather 🔫
# ==============================================================================
async def mybot():
    """
    تم تعطيل التعامل مع BotFather نهائياً.
    """
    print("mikey: 🛑 تجاوزنا BotFather.. البوت المساعد تم إعداده في setup_bot.")
    pass


async def add_bot_to_logger_group(chat_id):
    """
    To add bot to logger groups
    """
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


# تم تعطيل القائمة القديمة لتفادي الأخطاء
zthon = {} 

async def saves():
    # mikey: تم إعدام هذه الدالة لأنها تسبب مشاكل اتصال
    print("mikey: 🛑 saves() skipped.")
    pass


async def load_plugins(folder, extfolder=None):
    """
    To load plugins from the mentioned folder
    """
    # mikey: إضافة glob و os هنا لتفادي الأخطاء
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
        # ==================================================
        # mikey: المصلح الآلي (Auto-Fixer)
        # ==================================================
        try:
            with open(name, "r", encoding='utf-8', errors='ignore') as f:
                content = f.read()
            modified = False
            if "‚" in content:
                content = content.replace("‚", ",")
                modified = True
            # اذا الملف يستخدم zedub وما استدعاه
            if "zedub" in content and "from zthon.core.session import zedub" not in content:
                content = "from zthon.core.session import zedub\n" + content
                modified = True
            
            if modified:
                with open(name, "w", encoding='utf-8') as f:
                    f.write(content)
        except:
            pass
        # ==================================================

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
                            # LOGS.info(f"تم تحميل {shortname}")
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                        except Exception as e:
                            if shortname not in failure:
                                failure.append(shortname)
                            LOGS.info(f"فشل تحميل {shortname}: {e}")
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                LOGS.info(
                    f"لا يمكنني تحميل {shortname} بسبب الخطأ {e}\nمجلد القاعده {plugin_path}"
                )
    if extfolder:
        if not failure:
            failure.append("None")
        await zedub.tgbot.send_message(
            BOTLOG_CHATID,
            f'Your external repo plugins have imported \n**No of imported plugins :** `{success}`\n**Failed plugins to import :** `{", ".join(failure)}`',
        )


# ==============================================================================
# mikey: دالة التحقق من القناة (المعدلة جذرياً)
# بدلاً من الإنشاء، تقوم بالتحقق والتحديث فقط.
# ==============================================================================
async def verifyLoggerGroup():
    """
    التحقق من وجود القناة وتحديثها، والصراخ إذا كانت مفقودة.
    """
    print("mikey: 🧐 جاري فحص القناة من ريندر...")
    
    # 1. سحب الآيدي من المتغيرات
    logger_id_str = os.environ.get("PRIVATE_GROUP_ID")
    
    if not logger_id_str:
        LOGS.error("mikey: 🤬 وين القناة يا حيوان؟ حط PRIVATE_GROUP_ID في ريندر!")
        sys.exit(1)
        
    try:
        # تحويل الآيدي لرقم
        logger_id = int(logger_id_str)
    except ValueError:
        LOGS.error(f"mikey: 🤬 الآيدي '{logger_id_str}' مو رقم! تأكد منه.")
        sys.exit(1)

    # 2. تثبيت القيم في الذاكرة والداتابيس
    Config.PRIVATE_GROUP_ID = logger_id
    Config.PRIVATE_GROUP_BOT_API_ID = logger_id
    Config.BOTLOG_CHATID = logger_id
    Config.PM_LOGGER_GROUP_ID = logger_id
    
    # حفظ في SQL اذا كان موجود
    try:
        addgvar("PRIVATE_GROUP_BOT_API_ID", logger_id)
        addgvar("PM_LOGGER_GROUP_ID", logger_id)
        addgvar("BOTLOG_CHATID", logger_id)
    except:
        pass

    # 3. محاولة الدخول للقناة وتحديثها
    flag = False
    try:
        # محاولة جلب معلومات القناة
        entity = await zedub.get_entity(logger_id)
        print(f"mikey: ✅ تم العثور على القناة: {entity.title}")
        
        # تحديث الصورة (إذا توفرت)
        try:
            # هنا بنحط صورة افتراضية من ملفات السورس
            photo_path = "zthon/zilzal/refz.jpg"
            if os.path.exists(photo_path):
                await zedub(EditPhotoRequest(
                    channel=entity,
                    photo=await zedub.upload_file(photo_path)
                ))
                print("mikey: 📸 تم تحديث صورة القناة.")
        except Exception as e:
            print(f"mikey: ما قدرت أحدث الصورة (عادي): {e}")

        # تحديث الاسم
        try:
            await zedub(EditTitleRequest(
                channel=entity,
                title="Refz Source Storage 📦"
            ))
            print("mikey: ✏️ تم تحديث اسم القناة.")
        except Exception as e:
            print(f"mikey: ما قدرت أغير الاسم (عادي): {e}")
            
        # محاولة رفع البوت مشرف
        try:
            bot_info = await zedub.tgbot.get_me()
            await zedub(EditAdminRequest(
                channel=entity,
                user_id=bot_info.username,
                admin_rights=ChatAdminRights(
                    change_info=True, post_messages=True, edit_messages=True,
                    delete_messages=True, ban_users=True, invite_users=True,
                    pin_messages=True, add_admins=True, manage_call=True
                ),
                rank="Refz Helper"
            ))
            print("mikey: 👮‍♂️ تم رفع البوت مشرف في القناة.")
        except Exception as e:
             print(f"mikey: ما قدرت أرفع البوت مشرف (يمكن ما عندي صلاحية): {e}")

        flag = True

    except ValueError:
        LOGS.error("mikey: ❌ البوت مو قادر يشوف القناة! تأكد إنك ضفت حسابك فيها.")
        # لن ننشئ جديد، سنخرج
        sys.exit(1)
    except Exception as e:
        LOGS.error(f"mikey: ❌ خطأ غريب في القناة: {e}")
        sys.exit(1)

    # 4. تشغيل البوت إذا كل شي تمام
    if flag:
        # استخدام الطريقة الذكية لتشغيل الموديول الرئيسي
        # executable = sys.executable.replace(" ", "\\ ")
        # args = [executable, "-m", "zthon"]
        # os.execle(executable, *args, os.environ)
        # sys.exit(0)
        
        # mikey: بدال ما نعيد تشغيل السكربت وندخل في لوب، نخليه يكمل
        print("mikey: 🚀 كل شي جاهز، الإقلاع مستمر...")
        return


async def install_externalrepo(repo, branch, cfolder):
    zedREPO = repo
    rpath = os.path.join(cfolder, "requirements.txt")
    if zedBRANCH := branch:
        repourl = os.path.join(zedREPO, f"tree/{zedBRANCH}")
        gcmd = f"git clone -b {zedBRANCH} {zedREPO} {cfolder}"
        errtext = f"There is no branch with name `{zedBRANCH}` in your external repo {zedREPO}."
    else:
        repourl = zedREPO
        gcmd = f"git clone {zedREPO} {cfolder}"
        errtext = f"The link({zedREPO}) you provided for `EXTERNAL_REPO` is invalid."

    try:
        response = urllib.request.urlopen(repourl)
        if response.code != 200:
            LOGS.error(errtext)
            return await zedub.tgbot.send_message(BOTLOG_CHATID, errtext)
    except:
        pass # تجاوز اخطاء الشبكة

    await runcmd(gcmd)
    if not os.path.exists(cfolder):
        LOGS.error("- حدث خطأ اثناء استدعاء رابط الملفات الاضافية...")
        return await zedub.tgbot.send_message(BOTLOG_CHATID, "**- حدث خطأ اثناء استدعاء رابط الملفات الاضافية...**")

    if os.path.exists(rpath):
        await runcmd(f"pip3 install --no-cache-dir -r {rpath}")

    await load_plugins(folder="zthon", extfolder=cfolder)