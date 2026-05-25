from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message
from Devil.handler_utils import handle_upload


@Client.on_message(filters.photo)
async def getimage(client, message: Message):
    await handle_upload(client, message, ext=".jpg", file_type="photo")
    raise StopPropagation
