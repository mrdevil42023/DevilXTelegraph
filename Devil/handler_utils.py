"""Shared helper for all file upload handlers."""
import os
import shutil
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from upload_helper import upload_file
from db import add_chat, record_upload

EX = "UPLOADS"

FOOTER = (
    "\n\n🖥 THIS BOT IS CREATED BY [MR DEVIL](http://t.me/mrdevil12)"
    "\nFOR UPDATE JOIN OUR CHANNEL [DEVIL BOT'S](https://t.me/devilbots971)"
)

HOST_EMOJIS = {
    "Catbox":      "📦",
    "0x0.st":      "🔗",
    "Uguu.se":     "🌐",
    "GoFile":      "☁️",
    "Transfer.sh": "🚀",
}


def _build_reply(results: list[tuple[str, str]]) -> tuple[str, InlineKeyboardMarkup]:
    """Build message text and share buttons for multiple upload results."""
    lines = ["**✅ Upload Complete! Your links:**\n"]
    buttons = []
    for host, url in results:
        emoji = HOST_EMOJIS.get(host, "🔗")
        lines.append(f"{emoji} **{host}:** `{url}`")
        buttons.append([InlineKeyboardButton(f"👓 Share via {host}", url=f"https://telegram.me/share/url?url={url}")])

    text = "\n".join(lines) + FOOTER
    markup = InlineKeyboardMarkup(buttons)
    return text, markup


async def handle_upload(client, message: Message, ext: str, file_type: str):
    """
    Generic file upload handler.
    ext      — file extension e.g. ".jpg"
    file_type — one of: photo / document / video / audio
    """
    import uuid

    chat_id = str(message.chat.id)
    tmp_dir = os.path.join(EX, chat_id)
    os.makedirs(tmp_dir, exist_ok=True)
    file_path = os.path.join(tmp_dir, str(uuid.uuid4()) + ext)

    status = await message.reply_text("⏳ Downloading & uploading to all hosts... Please wait.")

    try:
        file_path = await client.download_media(message=message, file_name=file_path)
        if message.from_user:
            add_chat(message.from_user.id, "private", message.from_user.first_name)

        await status.edit_text("📨 Uploading to multiple hosts simultaneously...")

        results = upload_file(file_path)
        record_upload(file_type)

        text, markup = _build_reply(results)
        await status.edit_text(text, disable_web_page_preview=True, reply_markup=markup)

    except Exception as e:
        await status.edit_text(f"❌ Upload failed:\n`{e}`\n\nPlease retry in a few seconds.")
    finally:
        try:
            shutil.rmtree(tmp_dir)
        except Exception:
            pass
