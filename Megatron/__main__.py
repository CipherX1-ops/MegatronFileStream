import asyncio
import logging
import requests
from flask import Flask, request, redirect
from aiohttp import web

from pyrogram import idle

from .vars import Var 
from Megatron import utils
from Megatron import bot_info
from Megatron.server import web_server
from Megatron.bot.clients import initialize_clients


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

loop = asyncio.get_event_loop()

vector = Flask(__name__)

@vector.route("/")
async def main():
    headers_list = request.headers.getlist("X-Forwarded-For")
    user_ip = headers_list[0] if headers_list else request.remote_addr
    url = f"http://ip-api.com/json/{user_ip}?fields=message,country,regionName,city,lat,lon,isp,as,mobile,proxy,hosting,query"
    response = requests.get(url)
    info = response.json()
    tracker = f"""*✨ IP Address:* {info['query']}
    *✨ Country:* `{info['country']}`
    *✨ Region Name:* `{info['regionName']}`
    *✨ City:* `{info['city']}`
    *✨ Latitude:* `{info['lat']}`
    *✨ Longitude:* `{info['lon']}`
    *✨ ISP:* `{info['isp']}`
    *✨ As:* `{info['as']}`
    *✨ User on Mobile:* `{info['mobile']}`
    *✨ Proxy:* `{info['proxy']}`
    *✨ Hosting:* `{info['hosting']}`
    """

async def start_services():
    print("----------------------------- DONE -----------------------------")
    print()
    print(
        "----------------------------- Initializing Clients -----------------------------"
    )
    await initialize_clients()
    print("----------------------------- DONE -----------------------------")
    if Var.ON_HEROKU:
        print("------------------ Starting Keep Alive Service ------------------")
        print()
        asyncio.create_task(utils.ping_server())
    print("-------------------- Initalizing Web Server --------------------")
    await vector.run(host="0.0.0.0" if Var.ON_HEROKU else Var.BIND_ADDRESS , debug=False)
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0" if Var.ON_HEROKU else Var.BIND_ADDRESS
    await web.TCPSite(app, bind_address, Var.PORT).start()
    print("----------------------------- DONE -----------------------------")
    print()
    print("----------------------- Service Started -----------------------")
    print("                        bot =>> {}".format(bot_info.first_name))
    if bot_info.dc_id:
        print("                        DC ID =>> {}".format(str(bot_info.dc_id)))
    print("                        server ip =>> {}".format(bind_address, Var.PORT))
    if Var.ON_HEROKU:
        print("                        app running on =>> {}".format(Var.FQDN))
    print("---------------------------------------------------------------")
    await idle()


if __name__ == "__main__":
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        logging.info("----------------------- Service Stopped -----------------------")
