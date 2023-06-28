import os
import signal
import sys
import asyncio
import logging
from .vars import Var
from aiohttp import web
from pyrogram import idle
from Megatron import utils
from Megatron import StreamBot
from Megatron.server import web_server
from Megatron.bot.clients import initialize_clients


logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="[%(asctime)s][%(levelname)s] => %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout),
              logging.FileHandler("streambot.log", mode="a", encoding="utf-8")],)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

server = web.AppRunner(web_server())

if sys.version_info[1] > 9:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()
    

async def start_services():
    print()
    print("-------------------- Initializing Telegram Bot --------------------")
    await StreamBot.start()
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    print("------------------------------ DONE ------------------------------")
    print()
    print(
        "---------------------- Initializing Clients ----------------------"
    )
    await initialize_clients()
    print("------------------------------ DONE ------------------------------")
    if Var.ON_HEROKU:
        print("------------------ Starting Keep Alive Service ------------------")
        print()
        asyncio.create_task(utils.ping_server())
    print("--------------------- Initalizing Web Server ---------------------")
    await server.setup()
    bind_address = "0.0.0.0" if Var.ON_HEROKU else Var.BIND_ADDRESS
    await web.TCPSite(server, bind_address, Var.PORT).start()
    print("------------------------------ DONE ------------------------------")
    print()
    print("------------------------- Service Started -------------------------")
    print("                        bot =>> {}".format(bot_info.first_name))
    if bot_info.dc_id:
        print("                        DC ID =>> {}".format(str(bot_info.dc_id)))
    print("                        server ip =>> {}".format(bind_address, Var.PORT))
    if Var.ON_HEROKU:
        print("                        app running on =>> {}".format(Var.FQDN))
    print("------------------------------------------------------------------")
    await idle()

#async def cleanup():
    #await server.cleanup()
    #if StreamBot.is_connected:
        #await StreamBot.stop()
        
#async def handle_termination(signum, frame):
    #print("Received termination signal")
    #await cleanup()
    #sys.exit(0)
    
if __name__ == "__main__":
    #signal.signal(signal.SIGINT, lambda s,f: asyncio.ensure_future(handle_termination(s,f)))
    #signal.signal(signal.SIGTERM, lambda s,f: asyncio.ensure_future(handle_termination(s,f)))
    try:
        loop.run_until_complete(start_services())
        #loop.run_forever()
    except KeyboardInterrupt:
        print("------------------------ Stopped Services ------------------------")
