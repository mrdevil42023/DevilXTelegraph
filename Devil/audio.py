from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message
from Devil.handler_utils import handle_upload


@Client.on_message(filters.audio)
async def getdocument_audio(client, message: Message):
    await handle_upload(client, message, ext=".mp3", file_type="audio")
    raise StopPropagation
