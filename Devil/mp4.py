from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message
from Devil.handler_utils import handle_upload


@Client.on_message(filters.video)
async def getdocument_video(client, message: Message):
    await handle_upload(client, message, ext=".mp4", file_type="video")
    raise StopPropagation
