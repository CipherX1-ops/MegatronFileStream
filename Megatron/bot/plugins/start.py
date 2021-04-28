from Megatron.bot import StreamBot
from Megatron.vars import Var
from Megatron.utils.human_readable import humanbytes
from Megatron.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started the bot."
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL is not None:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="Sorry, You are Banned to use me. Contact my [Support Group](https://t.me/joinchat/riq-psSksFtiMDU8).",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Please join updates channel to use me**\nOnly channel subscribers can use the bot\nAfter joining tap help button\n\n✨لطفا در چنل عضو شوید. تنها اعضای چنل می توانند از بات استفاده کنند.\nپس از عضویت بر روی /help کلیک کنید.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("✵ Join Updates Channel ✵", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="Something went Wrong. Contact my [Support Group](https://t.me/joinchat/riq-psSksFtiMDU8).",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return
        await m.reply_text(
            text="Hey Dear 🙋🏻‍♂️\nI'm Telegram File to Link Generator Bot.\n\nSend me any file & get the fast direct download link!\n\nسلام کاربر عزیز 🙋🏻‍♂️\nمن بات تبدیل فایل به لینک هستم\nفایل تلگرامی خود را ارسال کنید تا لینک دانلود پر سرعت آن را دریافت نمایید ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('✵ Updates Channel ✵', url='https://t.me/FutureTechnologyOfficial'), InlineKeyboardButton('✵ Support Group ✵', url='https://t.me/joinchat/riq-psSksFtiMDU8')],
                    [InlineKeyboardButton('✵ Developer ✵', url='https://t.me/CipherXBot')]
                ]
            ),
            disable_web_page_preview=True
        )
    else:
        if Var.UPDATES_CHANNEL is not None:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/joinchat/riq-psSksFtiMDU8).",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="****Please join updates channel to use me**\nOnly channel subscribers can use the bot\nAfter joining tap help button\n\n✨لطفا در چنل عضو شوید. تنها اعضای چنل می توانند از بات استفاده کنند.\nپس از عضویت بر روی /help کلیک کنید.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("✵ Join Updates Channel ✵", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ],
                            [
                                InlineKeyboardButton("🔄 Refresh / Try Again",
                                                     url=f"https://t.me/FiletoLinkTelegramBot?start=FutureTechnologyOfficial_{usr_cmd}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="Something went Wrong. Contact my [Support Group](https://t.me/joinchat/riq-psSksFtiMDU8).",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))

        file_size = None
        if get_msg.video:
            file_size = f"{humanbytes(get_msg.video.file_size)}"
        elif get_msg.document:
            file_size = f"{humanbytes(get_msg.document.file_size)}"
        elif get_msg.audio:
            file_size = f"{humanbytes(get_msg.audio.file_size)}"

        file_name = None
        if get_msg.video:
            file_name = f"{get_msg.video.file_name}"
        elif get_msg.document:
            file_name = f"{get_msg.document.file_name}"
        elif get_msg.audio:
            file_name = f"{get_msg.audio.file_name}"

        stream_link = "https://{}/{}/{}".format(Var.FQDN, get_msg.message_id, file_name) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.message_id,
                                     file_name)

        msg_text = "Your Link Generated! 😄\n\nلینک پر سرعت شما ایجاد شد! 😄\n\n📂 **File Name:** `{}`\n**File Size:** `{}`\n\n📥 **Download Link:** `{}`"
        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✵ Download Now ✵", url=stream_link)]])
        )


@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) Started !!"
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Sorry, You are Banned to use me. Contact my [Support Group](https://t.me/joinchat/riq-psSksFtiMDU8).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="****Please join updates channel to use me**\nOnly channel subscribers can use the bot\nAfter joining tap help button\n\n✨لطفا در چنل عضو شوید. تنها اعضای چنل می توانند از بات استفاده کنند.\nپس از عضویت بر روی /help کلیک کنید.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("✵ Join Updates Channel ✵", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Something went Wrong. Contact my [Support Group](https://t.me/joinchat/riq-psSksFtiMDU8).",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text="✨ Send me any file, I'll give you its direct download link\n\nAlso I'm supported in channels. Add me to channel as admin to make me workable\n\n✨ فایل تلگرامی خود را برای من بفرستید تا لینک دانلود مستقیم آن را برای شما بفرستم\n\nهمچنین با ارتقای من به عنوان ادمین در چنل خود می توانید از امکانات من استفاده کنید، بدین صورت که در زمان پست فایل جدید در چنل دکمه شیشه ای دریافت لینک مستقیم فایل پست شده در زیر پست ایجاد می گردد.",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("✵ Support Group ✵", url="https://t.me/joinchat/riq-psSksFtiMDU8"), InlineKeyboardButton("✵ Update Channel ✵", url="https://t.me/FutureTechnologyOfficial")],
                [InlineKeyboardButton("✵ Developer ✵", url="https://t.me/CipherXBot")]
            ]
        )
    )
