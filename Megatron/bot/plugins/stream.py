import asyncio
import logging
from urllib.parse import quote_plus

from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Megatron.bot import StreamBot
from Megatron.utils import get_hash, get_name
from Megatron.utils.database import Database
from Megatron.handlers.fsub import force_subscribe
from Megatron.vars import Var 
from Megatron.utils.human_readable import humanbytes
from Megatron.utils.antispam import check_spam
from Megatron.strings import get_string

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


def detect_type(m: Message):
    if m.document:
        return m.document
    elif m.video:
        return m.video
    elif m.photo:
        return m.photo
    elif m.audio:
        return m.audio
    else:
        return

@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)
async def media_receive_handler(c: Client, m: Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started the bot."
        )
    if Var.UPDATES_CHANNEL:
        fsub = await force_subscribe(c, m)
        if fsub == 400:
            return    

    file_size = None
    if m.video:
        file_size = f"{humanbytes(m.video.file_size)}"
    elif m.document:
        file_size = f"{humanbytes(m.document.file_size)}"
    elif m.audio:
        file_size = f"{humanbytes(m.audio.file_size)}"
    elif m.photo:
        file_size = f"{humanbytes(m.photo.file_size)}"

    file_name = None
    if m.video:
        file_name = f"{m.video.file_name}"
    elif m.document:
        file_name = f"{m.document.file_name}"
    elif m.audio:
        file_name = f"{m.audio.file_name}"
    elif m.photo:
        file_name = f"{m.photo.file_id}"

    try:
        file = detect_type(m)
        file_name = ''
        if file and "GiB" in str(file_size) and not m.from_user.id in Var.PRO_USERS:
            await c.send_message(m.chat.id, get_string("limit"))
        else:
            is_spam, sleep_time = await check_spam(m.from_user.id)
            if is_spam:
                if m.from_user.id in Var.PRO_USERS:
                    await m.reply_text(get_string("pro").format(str(sleep_time), str(sleep_time)), quote=True)
                else:
                    await m.reply_text(get_string("usual").format(str(sleep_time), str(sleep_time)), quote=True)
            else:
                u = await c.get_chat_member(int(Var.UPDATES_CHANNEL), m.from_user.id)
                if u.status == "kicked" or u.status == "banned":
                    await c.send_message(
                        chat_id=m.from_user.id,
                        text=get_string("banned"),
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                else:
                    file_name = file.file_name
                    user_type = "#Pro_User" if m.from_user.id in Var.PRO_USERS else "#Ordinary_User" 
                    log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
                    stream_link = f"{Var.URL}{log_msg.message_id}/{quote_plus(get_name(m))}?hash={get_hash(log_msg)}"
                    short_link = f"{Var.URL}{get_hash(log_msg)}{log_msg.message_id}"
                    logging.info(f"Generated link: {stream_link} for {m.from_user.first_name}")
                    await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"✨ **Requested by:** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n✨ **User ID:** `{m.from_user.id}`\n✨ **User Type:** `{user_type}`\n✨ **Download Link:** {stream_link}\n✨ **Short Link:** {short_link}", disable_web_page_preview=True, reply_to_message_id=log_msg.message_id, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("࿋ Ban User ࿋", callback_data=f"ban_{m.from_user.id}")]])) 
                    await m.reply_text(
                        text=get_string("stream").format(file_name, file_size, stream_link, short_link)
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("࿋ Direct/Stream Link ࿋", url=stream_link)],
                                [InlineKeyboardButton("࿋ Short Link ࿋", url=short_link)],
                            ],
                        ),
                        quote=True, 
                        parse_mode="Markdown"
                    )
            
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Got FloodWait of {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**User ID:** `{str(m.from_user.id)}`", disable_web_page_preview=True, parse_mode="Markdown")


@StreamBot.on_message(filters.channel & (filters.document | filters.video | filters.photo) & ~filters.edited & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}{log_msg.message_id}/{quote_plus(get_name(broadcast))}?hash={get_hash(log_msg)}"
        await log_msg.reply_text(
            text=f"**Channel Name:** `{broadcast.chat.title}`\n**Channel ID:** `{broadcast.chat.id}`\n**Link:** {stream_link}",
            quote=True,
            parse_mode="Markdown"
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("࿋ Direct Download Link ࿋", url=f"{stream_link}")]
                ]
            )
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"Got FloodWait of {str(w.x)}s from {broadcast.chat.title}\n\n**Channel ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True, parse_mode="Markdown")
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"#ERROR_TRACEBACK: `{e}`", disable_web_page_preview=True, parse_mode="Markdown")
