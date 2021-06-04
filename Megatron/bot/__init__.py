from pyrogram import Client
from pyromod import listen
from ..vars import Var

StreamBot = Client(
    session_name='Megatron',
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    bot_token=Var.BOT_TOKEN,
    sleep_threshold=Var.SLEEP_THRESHOLD,
    workers=Var.WORKERS
)
