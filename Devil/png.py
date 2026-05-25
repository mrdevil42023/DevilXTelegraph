from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message
from Devil.handler_utils import handle_upload


@Client.on_message(filters.document)
async def getimage_doc(client, message: Message):
    await handle_upload(client, message, ext=".png", file_type="document")
    raise StopPropagation
