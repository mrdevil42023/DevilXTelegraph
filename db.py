import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_client = None
_db_ok: bool = True
_warned: bool = False

# In-memory upload stats (always works, even without Supabase)
_upload_stats = {
    "photo": 0,
    "document": 0,
    "video": 0,
    "audio": 0,
}


def record_upload(file_type: str):
    """Record an upload in the in-memory stats. file_type: photo/document/video/audio"""
    if file_type in _upload_stats:
        _upload_stats[file_type] += 1


def get_upload_stats() -> dict:
    return dict(_upload_stats)


def _warn_once(msg: str):
    global _warned
    if not _warned:
        print(f"\n{'='*55}")
        print(f"  [DB WARNING] {msg}")
        print(f"  → Bot will still work, but stats/tracking disabled.")
        print(f"  → Fix: set SUPABASE_URL and SUPABASE_KEY secrets")
        print(f"{'='*55}\n")
        _warned = True


def get_client():
    global _client, _db_ok
    if not _db_ok:
        return None
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            _warn_once("SUPABASE_URL or SUPABASE_KEY is missing")
            _db_ok = False
            return None
        try:
            from supabase import create_client
            _client = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            _warn_once(f"Could not connect to Supabase: {e}")
            _db_ok = False
            return None
    return _client


def _check_key_error(e: Exception):
    msg = str(e).lower()
    if "invalid api key" in msg or "apikey" in msg or "unauthorized" in msg:
        _warn_once("Invalid Supabase API key — use the SERVICE ROLE secret key.")
        global _db_ok
        _db_ok = False


def add_chat(chat_id: int, chat_type: str, title: str = None):
    global _db_ok
    if not _db_ok:
        return
    try:
        c = get_client()
        if c is None:
            return
        c.table("chats").upsert({
            "chat_id": chat_id,
            "chat_type": chat_type,
            "title": title or ""
        }).execute()
    except Exception as e:
        _check_key_error(e)
        if _db_ok:
            print(f"[DB] add_chat error: {e}")


def get_all_chats():
    if not _db_ok:
        return []
    try:
        c = get_client()
        if c is None:
            return []
        res = c.table("chats").select("chat_id").execute()
        return [row["chat_id"] for row in res.data]
    except Exception as e:
        _check_key_error(e)
        return []


def chat_count():
    if not _db_ok:
        return 0
    try:
        c = get_client()
        if c is None:
            return 0
        res = c.table("chats").select("chat_id", count="exact").execute()
        return res.count
    except Exception as e:
        _check_key_error(e)
        return 0


def user_count():
    if not _db_ok:
        return 0
    try:
        c = get_client()
        if c is None:
            return 0
        res = c.table("chats").select("chat_id", count="exact").eq("chat_type", "private").execute()
        return res.count
    except Exception as e:
        _check_key_error(e)
        return 0
