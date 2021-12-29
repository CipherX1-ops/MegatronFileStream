import asyncio 
import logging
import aiohttp
import traceback
from os import environ

from Megatron.vars import Var 

async def ping_server():
    sleep_time = Var.PING_INTERVAL
    while True:
        await asyncio.sleep(sleep_time) 
        try:
            session = aiohttp.ClientSession(raise_for_status=True)
            x = await session.get(Var.URL, raise_for_status=False)
            async with x:
                if x.status == 200:
                    logging.info(f"Bot is working fine. Pinged server with response code : {x.status}") 
                else:
                    if 'DYNO' in environ: 
                        try:
                            heroku = heroku3.from_key(Var.HEROKU_API_KEY)
                            app = heroku.app(Var.APP_NAME)
                            app.restart()
                            logging.info("Successfully restarted the app for pinging...") 
                        except Exception as e:
                            logging.warning(f"Failed to restart the app because of this error : {str(e)}") 
                    else:
                        logging.warning("Failed to ping the server...!")

