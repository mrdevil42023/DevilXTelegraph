from pyrogram import Client as mapple, idle
from auth import Vauth
import logging
import shutil
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

BOT_TOKEN = Vauth.BOT_TOKEN
API_ID = Vauth.API_ID
API_HASH = Vauth.API_HASH

PLUGINS = dict(
    root="Devil",
)

EX = "UPLOADS"

app = mapple(
    "DevilXTelegraph",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=PLUGINS,
    workers=10,
    workdir=os.getcwd()
)
app.start()
try:
    shutil.rmtree(EX)
except Exception:
    pass
idle()
app.stop()
try:
    shutil.rmtree(EX)
except Exception:
    pass
