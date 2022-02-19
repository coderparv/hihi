import time, re, psutil
from platform import python_version

from sys import argv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import escape_markdown, mention_html
from Yone.Handlers.validation import is_user_admin

from telegram.error import (
    BadRequest,
    Unauthorized,
)

from Yone import (
    OWNER_ID,
    OWNER_USERNAME,
    dispatcher, 
    StartTime,
    LOGGER,
    SUPPORT_CHAT,
    WEBHOOK,
    CERT_PATH,
    PORT,
    URL,
    TOKEN,
    PHOTO,
    telethn,
    updater)

from Yone.Plugins import ALL_MODULES
from Yone.__help__ import (
get_help, 
help_button, 
get_settings, 
settings_button, 
migrate_chats, 
send_help, 
send_admin_help,
send_user_help,
user_help_button,
send_settings,
admin_help_button,
tools_help_button,
send_tools_help,
HELP_STRINGS,
IMPORTED,
IMPORTED,
HELPABLE,
ADMIN,
USER,
TOOLS )


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = """ Hello student *{}*, 
My Self [XYZ BOOKS🤖](https://t.me/codesfru/35) 
made for your service related to educational sort.

HIGHLIGHTS 👇

‣ Updating you on latest books posted.
‣ You will get every possible thing related to CBSE , JEE and NEET exams here .

NOW WHY ARE YOU WAITING?

*GO TO THE BUTTONS BELOW TO ACCESS ALL EDUCATIONAL STUFFS💝✨.*
"""




def start(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    first_name = update.effective_user.first_name
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK", callback_data="help_back")]]
                    ),
                )
                send_admin_help(
                    update.effective_chat.id,
                    ADMIN[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK", callback_data="admin_back")]]
                    ),
                )
                send_user_help(
                    update.effective_chat.id,
                    USER[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK", callback_data="user_back")]]
                    ),
                )
                send_tools_help(
                    update.effective_chat.id,
                    USER[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK", callback_data="tools_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            update.effective_message.reply_text(
                PM_START_TEXT.format(
                        escape_markdown(first_name), escape_markdown(context.bot.first_name)),
                reply_markup=InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="BOOK STORE➕", url=f"https://t.me/+YVBwIkHbl7FhMjZl"),
    ],
    [
        InlineKeyboardButton(text=" ☑️CBSE XYZ", url="https://t.me/cbse_xyz"),
        InlineKeyboardButton(
            text="💝CBSE EXCLUSIVE", url="https://t.me/xyz_cbse"
        ),
    ],
    [
        InlineKeyboardButton(text="✔️JEE XYZ", url="https://t.me/jee_xyz"),
        InlineKeyboardButton(
            text="✔️NEET XYZ", url="https://t.me/NEET_XYZ"
        ),
    ],
    [
        InlineKeyboardButton(text="Click on me for more✨", callback_data="yone_"),
    ],
]),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
            text = (
                f"Hello {mention_html(user.id, user.first_name)}, I'm {bot.first_name}\n\n"
                f"┏━━━━━━━━━━━━━━━━━━━\n"
                f"┣[• Owner : @{OWNER_USERNAME}  \n"
                f"┣[• Uptime : {uptime} \n"
                f"┣[• Core : {psutil.cpu_percent()}%\n"
                f"┣[• Python   : Ver {python_version()} \n"
                f"┗━━━━━━━━━━━━━━━━━━━")
        

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="SUPPORT", 
                        url=f"https://t.me/{SUPPORT_CHAT}"),
                    InlineKeyboardButton(
                        text="DEVLOPER", 
                        url=f"https://t.me/{OWNER_USERNAME}")
                    
                ],
                
                ])
            message.reply_photo(
                        PHOTO,
                        caption=(text),
                        reply_markup=keyboard,
                        parse_mode=ParseMode.HTML,
                        
                    )

                



def yone_about_callback(update: Update, context: CallbackContext):
    first_name = update.effective_user.first_name
    query = update.callback_query
    if query.data == "yone_":
        query.message.edit_text(
            text="""Hello *{}*, My name is *{}*. 
I MADE FOR YOU WITH LOTS OF LOVE💚💙💜🖤❤️🧡💛 and hard work🔥 -
            \n 🎐 Free premium study stuff for you.
            \n 🎐 Act as a versatile source of materials and study stuff for CBSE .JEE AND NEET
            \n 🎐 please share me with you friend by copying this link 👉 https://t.me/xyzbookbot?startgroup=true 🍫
            \n 🎐 I will be keep updating you just keep me on pin in your chat.
            \n\n*If For more info and support check the links below don't forget to check LINK BOX🔗🎁*""".format(
                        escape_markdown(first_name), escape_markdown(context.bot.first_name)),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                   [
                     InlineKeyboardButton(text="Donwload our App⬇️", url="t.me/bookstoreplus"),
                     InlineKeyboardButton(text="🄳ivineӼNet", url="t.me/divinexnet"),
                   ],
                     [
                     InlineKeyboardButton(text="XYZ BOOKS SUPPORT💬", url="t.me/+-I2sy04aeEtjOTZl"),
                     InlineKeyboardButton(text="Creator🇮🇳", url="t.me/ALivefru"),
                   ],
                   [
                    InlineKeyboardButton(text="THE LINK BOX🎁", url="t.me/xyzlinkbox"),
                    InlineKeyboardButton(text="Back", callback_data="yone_back")
                   ]
                ]
            ),
        )
    elif query.data == "yone_back":
        query.message.edit_text(
                PM_START_TEXT.format(
                        escape_markdown(first_name), escape_markdown(context.bot.first_name)),
                reply_markup=InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="BOOK STORE➕", url=f"https://t.me/+YVBwIkHbl7FhMjZl"),
    ],
    [
        InlineKeyboardButton(text=" ☑️CBSE XYZ", url="https://t.me/cbse_xyz"),
        InlineKeyboardButton(
            text="💝CBSE EXCLUSIVE", url="https://t.me/xyz_cbse"
        ),
    ],
    [
        InlineKeyboardButton(text="✔️JEE XYZ", url="https://t.me/jee_xyz"),
        InlineKeyboardButton(
            text="✔️NEET XYZ", url="https://t.me/NEET_XYZ"
        ),
    ],
    [
        InlineKeyboardButton(text="Click on me for more✨", callback_data="yone_"),
    ],
]),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            stringz = "My dear Owner , I'm Working Again. Thanks to make me live."
            dispatcher.bot.sendMessage(f"@{OWNER_ID}", stringz)
        except Unauthorized:
            LOGGER.warning(
                "Bot isnt able to send message to support_chat, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    start_handler = CommandHandler("start", start, pass_args=True, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*", run_async=True)
    admin_help_callback_handler = CallbackQueryHandler(admin_help_button, pattern=r"admin_.*", run_async=True)
    user_help_callback_handler = CallbackQueryHandler(user_help_button, pattern=r"user_.*", run_async=True)
    tools_help_callback_handler = CallbackQueryHandler(tools_help_button, pattern=r"tools_.*", run_async=True)

    about_callback_handler = CallbackQueryHandler(yone_about_callback, pattern=r"yone_", run_async=True)

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_", run_async=True)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats, run_async=True)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(admin_help_callback_handler)
    dispatcher.add_handler(user_help_callback_handler)
    dispatcher.add_handler(tools_help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(allowed_updates=Update.ALL_TYPES, timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()



if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    main()
