import os
import time
import string
import random
import asyncio
import aiofiles
import datetime
import traceback

from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

from Megatron.bot import StreamBot
from Megatron.vars import Var
from Megatron.utils.broadcast_helper import main_broadcast_handler
from Megatron.utils.database import Database
 

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

broadcast_ids = {}


@StreamBot.on_message(filters.command("status") & filters.private & filters.user(Var.OWNER_ID) & ~filters.edited)
async def sts(c: Client, m: Message):
    total_users = await db.total_users_count()
    await m.reply_text(text=f"**Total Users in Database:** `{total_users}`", parse_mode="Markdown", quote=True)


@StreamBot.on_message(filters.private & filters.command("broadcast") & filters.user(Var.OWNER_ID) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db)
