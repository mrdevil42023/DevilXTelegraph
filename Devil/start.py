from pyrogram import StopPropagation
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters
from db import add_chat

joinButton = InlineKeyboardMarkup([
    [InlineKeyboardButton("😈 OWNER 😈", url="http://t.me/mrdevil12")],
    [InlineKeyboardButton("🔥 UPDATE CHANNEL 🔥", url="https://t.me/devilbots971")],
    [InlineKeyboardButton("🔥 SUPPORT GROUP 🔥", url="https://t.me/devilbotsupport")],
    [InlineKeyboardButton("📖 Help & Commands", switch_inline_query_current_chat="/help")],
])

@Client.on_message(filters.command("start"))
async def start(_, ryui: Message):
    add_chat(ryui.from_user.id, "private", ryui.from_user.first_name)
    user_and_chats = ryui.from_user.first_name
    await ryui.reply_photo(
        "https://graph.org/file/b609a772e749668d82661.jpg",
        reply_markup=joinButton,
        caption=f"""DEVIL X TELEGRAPH
HOW ARE YOU **_`{user_and_chats}`_**,

🏷 Image to URL bot can convert these below file types to [Catbox](https://catbox.moe) URL.
🏷 Just send photo either in compressed or uncompressed format
- `JPG`
- `JPEG`
- `PNG`
- `GIF` __(send as a document)__
- `Mp4` __(send as a document)__
- `Mp3` __(send as a document)__
🏷 Keep sending your required type files one by one.
🏷 Files more than 200mb are not supported.

🖥 THIS BOT IS CREATED BY [MR DEVIL](http://t.me/mrdevil12)
FOR UPDATE JOIN OUR CHANNEL [DEVIL BOT'S](https://t.me/devilbots971)""")
    raise StopPropagation
