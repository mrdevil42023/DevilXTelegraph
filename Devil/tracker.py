from pyrogram import Client, filters
from pyrogram.types import Message
from db import add_chat

@Client.on_message(filters.private & ~filters.command(["start", "ping", "users", "broadcast"]))
async def track_private(client: Client, message: Message):
    if message.from_user:
        add_chat(message.from_user.id, "private", message.from_user.first_name)

@Client.on_message(filters.new_chat_members)
async def track_group_join(client: Client, message: Message):
    me = await client.get_me()
    for member in message.new_chat_members:
        if member.id == me.id:
            chat = message.chat
            add_chat(chat.id, chat.type.value if hasattr(chat.type, 'value') else str(chat.type), chat.title)

@Client.on_message(filters.group | filters.channel)
async def track_group_message(client: Client, message: Message):
    chat = message.chat
    add_chat(chat.id, chat.type.value if hasattr(chat.type, 'value') else str(chat.type), chat.title)
