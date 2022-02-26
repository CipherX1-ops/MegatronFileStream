from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant

from Megatron.bot import StreamBot
from Megatron.vars import Var
from Megatron.utils.human_readable import humanbytes
from Megatron.utils.database import Database
from Megatron.handlers.fsub import force_subscribe
from Megatron.strings import get_string

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m : Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started the bot."
        )
    firstname = m.from_user.first_name
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL:
            fsub = await force_subscribe(b, m)
            if fsub == 400:
                return
        await m.reply(
            text=get_string("start").format(m.from_user.mention(style="md")),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('✵ Updates Channel ✵', url='https://t.me/FutureTechnologyOfficial'), InlineKeyboardButton('✵ Support Group ✵', url='https://t.me/joinchat/riq-psSksFtiMDU8')],
                    [InlineKeyboardButton('✵ Developer ✵', url='https://t.me/CipherXBot')]
                ]
            ),
            disable_web_page_preview=True
        )
    else:
        if Var.UPDATES_CHANNEL:
            fsub = await force_subscribe(b, m)
            if fsub == 400:
                return
        u = await b.get_chat_member(int(Var.UPDATES_CHANNEL), m.from_user.id)
        if u.status == "kicked" or u.status == "banned":
            await b.send_message(
                chat_id=m.from_user.id,
                text=get_string("banned"),
                parse_mode="markdown",
                disable_web_page_preview=True
            )

@StreamBot.on_message(filters.command('upgrade') & filters.private & ~filters.edited)
async def upgrade(b, m : Message):
    await m.reply(
        text=get_string("pay"),
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('✨ Buy & Contact ✨', url='https://t.me/CipherXBot')]
            ]
        ),
        disable_web_page_preview=True
    )

@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(b, m : Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started !!"
        )
    if Var.UPDATES_CHANNEL:
        fsub = await force_subscribe(b, m)
        if fsub == 400:
            return
    u = await b.get_chat_member(int(Var.UPDATES_CHANNEL), m.from_user.id)
    if u.status == "kicked" or u.status == "banned":
        await b.send_message(
            chat_id=m.from_user.id,
            text=get_string("banned"),
            parse_mode="markdown",
            disable_web_page_preview=True
        )
    else:
        await m.reply_text(
            text=get_string("help"),
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("✵ Support Group ✵", url="https://t.me/joinchat/riq-psSksFtiMDU8"), InlineKeyboardButton("✵ Update Channel ✵", url="https://t.me/FutureTechnologyOfficial")],
                    [InlineKeyboardButton("✵ Developer ✵", url="https://t.me/CipherXBot")]
                ]
            )
        )
