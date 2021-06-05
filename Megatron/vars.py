from os import getenv, environ
from dotenv import load_dotenv

load_dotenv()


class Var(object):
    API_ID = int(getenv('API_ID', 1222520))
    API_HASH = str(getenv('API_HASH', '7e7e46cdd61842035fb191013f0a2387'))
    BOT_TOKEN = str(getenv('BOT_TOKEN', '1489398806:AAFV7_v2UxCGXavz0kjFV6L2CjiUHA7KNmI'))
    SESSION_NAME = str(getenv('SESSION_NAME', 'Megatron'))
    SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
    WORKERS = int(getenv('WORKERS', '4'))
    BIN_CHANNEL = int(getenv('BIN_CHANNEL', -1001452480828))
    PORT = int(getenv('PORT', 8080))
    BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
    OWNER_ID = int(getenv('OWNER_ID', '1601105531'))
    NO_PORT = bool(getenv('NO_PORT', False))
    APP_NAME = None
    if 'DYNO' in environ:
        ON_HEROKU = True
        APP_NAME = str(getenv('APP_NAME'))
    else:
        ON_HEROKU = False
    FQDN = str(getenv('FQDN', BIND_ADRESS)) if not ON_HEROKU else APP_NAME+'.herokuapp.com'
    DATABASE_URL = str(getenv('DATABASE_URL', 'mongodb+srv://cipherx:cipherx@cipherx.suvut.mongodb.net/cipherxretryWrites=true&w=majority'))
    UPDATES_CHANNEL = str(getenv('UPDATES_CHANNEL', 'FutureTechnologyOfficial'))
    BANNED_CHANNELS = list(set(int(x) for x in str(getenv("BANNED_CHANNELS", "-100")).split()))
    URL = "https://{}/".format(FQDN) if ON_HEROKU or NO_PORT else \
        "http://{}:{}/".format(FQDN, PORT)
