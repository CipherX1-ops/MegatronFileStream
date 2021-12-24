import asyncio
import logging
from urllib.parse import quote_plus

from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Megatron.bot import StreamBot
from Megatron.utils.database import Database
from Megatron.utils.human_readable import humanbytes
from Megatron.handlers.fsub import force_subscribe
from Megatron.vars import Var 

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

@StreamBot.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.photo) & ~filters.edited, group=4)
async def private_receive_handler(c: Client, m: Message):
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
        if file:
            file_name = file.file_name
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}{log_msg.message_id}"
        if file_name:
            stream_link += f'/{quote_plus(file_name)}'
        logging.info(f"Generated link: {stream_link} for {m.from_user.first_name}")
        msg_text = "Your Link Generated! 😄\n\nلینک پر سرعت شما ایجاد شد! 😄\n\n📂 **File Name:** `{}`\n**✨ File Size:** `{}`\n\n📥 **Download Link:** `{}`"
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Requested by [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**User ID:** `{m.from_user.id}`\n**Download Link:** {stream_link}", disable_web_page_preview=True, reply_to_message_id=log_msg.message_id, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ban User", callback_data=f"ban_{m.from_user.id}")]])) 
        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download Now", url=stream_link)]]),
            quote=True
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Got FloodWait of {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**User ID:** `{str(m.from_user.id)}`", disable_web_page_preview=True, parse_mode="Markdown")


@StreamBot.on_message(filters.channel & (filters.document | filters.video) & ~filters.edited, group=-1)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        await log_msg.reply_text(
            text=f"**Channel Name:** `{broadcast.chat.title}`\n**Channel ID:** `{broadcast.chat.id}`\n**Link:** https://t.me/FiletoLinkTelegramBot?start=FutureTechnologyOfficial_{str(log_msg.message_id)}",
            quote=True,
            parse_mode="Markdown"
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("✵ Direct Download Link ✵", url=f"https://t.me/FiletoLinkTelegramBot?start=FutureTechnologyOfficial_{str(log_msg.message_id)}")]
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
