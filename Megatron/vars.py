import os
from os import getenv, environ
from dotenv import load_dotenv

load_dotenv()


class Var(object):
    API_ID = int(getenv('API_ID'))
    API_HASH = str(getenv('API_HASH'))
    BOT_TOKEN = str(getenv('BOT_TOKEN'))
    BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", False))
    SESSION_NAME = str(getenv('SESSION_NAME', 'Megatron'))
    SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
    WORKERS = int(getenv('WORKERS', '4'))
    BIN_CHANNEL = int(getenv('BIN_CHANNEL'))
    PORT = int(getenv('PORT', 8000))
    BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
    PING_INTERVAL = int(getenv('PING_INTERVAL', '1200')) # 20 minutes
    HAS_SSL = getenv('HAS_SSL', False)
    HAS_SSL = True if str(HAS_SSL).lower() == 'true' else False
    OWNER_ID = int(getenv('OWNER_ID'))
    NO_PORT = getenv('NO_PORT', False)
    NO_PORT = True if str(NO_PORT).lower() == 'true' else False
    APP_NAME = None
    if 'DYNO' in environ:
        ON_HEROKU = True
        APP_NAME = str(getenv('APP_NAME'))
    else:
        ON_HEROKU = False
    DATABASE_URL = str(getenv('DATABASE_URL'))
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", None)
    BANNED_CHANNELS = list(set(int(x) for x in str(getenv("BANNED_CHANNELS", "-100")).split()))
    FQDN = str(getenv('FQDN', BIND_ADRESS)) if not ON_HEROKU or getenv('FQDN') else APP_NAME + '.herokuapp.com'
    if ON_HEROKU:
        URL = f"https://{FQDN}/"     
    else:
        URL = "http{}://{}{}/".format('s' if HAS_SSL else '', FQDN, '' if NO_PORT else ':'+ str(PORT))
