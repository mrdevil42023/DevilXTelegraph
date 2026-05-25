import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from auth import Vauth
from db import get_all_chats, chat_count, user_count, get_upload_stats

START_TIME = time.time()


def get_uptime():
    seconds = int(time.time() - START_TIME)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)


@Client.on_message(filters.command("help"))
async def help_cmd(client: Client, message: Message):
    await message.reply_text(
        "📖 **Available Commands**\n\n"
        "──────────────────────\n"
        "📤 **File Uploading**\n"
        "Just send any supported file and the bot will upload it to **5 hosts** at once and give you all the direct links.\n\n"
        "Supported formats:\n"
        "• 🖼 Photos — JPG, JPEG, PNG (compressed or uncompressed)\n"
        "• 📄 Documents — PNG, GIF, any file (send as document)\n"
        "• 🎬 Videos — MP4 (send as document)\n"
        "• 🎵 Audio — MP3\n"
        "• ⚠️ Max file size: **200 MB**\n\n"
        "──────────────────────\n"
        "🤖 **Commands**\n\n"
        "/start — Welcome message & bot info\n"
        "/help — Show this help message\n"
        "/ping — Check bot latency & uptime\n"
        "/stats — Show upload counts by file type _(this session)_\n\n"
        "──────────────────────\n"
        "👑 **Owner Only**\n\n"
        "/users — View total users & chats\n"
        "/broadcast — Broadcast a message to all chats _(reply to a message)_\n\n"
        "──────────────────────\n"
        "☁️ **Upload Hosts**\n\n"
        "📦 Catbox.moe — Permanent\n"
        "🔗 0x0.st — Long-term\n"
        "🌐 Uguu.se — 48 hours\n"
        "☁️ GoFile — Permanent\n"
        "🚀 Transfer.sh — 14 days\n\n"
        "🖥 Created by [MR DEVIL](http://t.me/mrdevil12)",
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("ping"))
async def ping(client: Client, message: Message):
    start = time.time()
    sent = await message.reply_text("🏓 Pong!")
    latency = round((time.time() - start) * 1000, 2)
    total = chat_count()
    users = user_count()
    await sent.edit_text(
        f"🏓 **Pong!**\n\n"
        f"⚡ **Latency:** `{latency} ms`\n"
        f"⏱ **Uptime:** `{get_uptime()}`\n"
        f"👤 **Users:** `{users}`\n"
        f"💬 **Total Chats:** `{total}`\n\n"
        f"🇵​🇴​🇼​🇪​🇷​🇪​🇩​ 🇧​🇾​\n"
        f"[𝙈𝙍 𝘿𝙀𝙑𝙄𝙇](http://t.me/mrdevil12)",
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("stats"))
async def stats_cmd(client: Client, message: Message):
    s = get_upload_stats()
    total = sum(s.values())
    await message.reply_text(
        f"📊 **Upload Statistics** _(this session)_\n\n"
        f"🖼 **Photos:** `{s.get('photo', 0)}`\n"
        f"📄 **Documents:** `{s.get('document', 0)}`\n"
        f"🎬 **Videos:** `{s.get('video', 0)}`\n"
        f"🎵 **Audio:** `{s.get('audio', 0)}`\n"
        f"──────────────\n"
        f"📦 **Total Uploads:** `{total}`\n\n"
        f"🇵​🇴​🇼​🇪​🇷​🇪​🇩​ 🇧​🇾​\n"
        f"[𝙈𝙍 𝘿𝙀𝙑𝙄𝙇](http://t.me/mrdevil12)",
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("users"))
async def users_cmd(client: Client, message: Message):
    if message.from_user.id != Vauth.OWNER_ID:
        await message.reply_text("❌ You are not authorized to use this command.")
        return
    total = chat_count()
    users = user_count()
    await message.reply_text(
        f"📊 **Bot Statistics**\n\n"
        f"👤 **Private Users:** `{users}`\n"
        f"💬 **Total Chats:** `{total}` _(users + groups + channels)_\n\n"
        f"🇵​🇴​🇼​🇪​🇷​🇪​🇩​ 🇧​🇾​\n"
        f"[𝙈𝙍 𝘿𝙀𝙑𝙄𝙇](http://t.me/mrdevil12)",
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("broadcast"))
async def broadcast(client: Client, message: Message):
    if message.from_user.id != Vauth.OWNER_ID:
        await message.reply_text("❌ You are not authorized to use this command.")
        return
    if not message.reply_to_message:
        await message.reply_text(
            "⚠️ **Usage:** Reply to a message with /broadcast to forward it to all users, groups and channels."
        )
        return

    all_chats = get_all_chats()
    status = await message.reply_text(f"📢 Broadcasting to **{len(all_chats)}** chats...")
    success, failed = 0, 0

    for chat_id in all_chats:
        try:
            await message.reply_to_message.forward(int(chat_id))
            success += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)

    await status.edit_text(
        f"📢 **Broadcast Complete!**\n\n"
        f"✅ **Sent:** `{success}`\n"
        f"❌ **Failed:** `{failed}`\n"
        f"📊 **Total:** `{success + failed}`\n\n"
        f"🇵​🇴​🇼​🇪​🇷​🇪​🇩​ 🇧​🇾​\n"
        f"[𝙈𝙍 𝘿𝙀𝙑𝙄𝙇](http://t.me/mrdevil12)",
        disable_web_page_preview=True
    )
