import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def _require(name, hint=""):
    val = os.getenv(name)
    if not val:
        print(f"""
{'='*58}
  [ERROR] Missing required config: {name}
  {hint}

  You must set the following environment variables / secrets:

    BOT_TOKEN → get from @BotFather on Telegram
    API_ID    → get from https://my.telegram.org/apps
    API_HASH  → get from https://my.telegram.org/apps
    OWNER_ID  → send /start to @userinfobot on Telegram

{'='*58}
""")
        sys.exit(1)
    return val

class Vauth:
    BOT_TOKEN = _require("BOT_TOKEN")
    API_ID    = int(_require("API_ID"))
    API_HASH  = _require("API_HASH")
    OWNER_ID  = int(os.getenv("OWNER_ID", "0"))
