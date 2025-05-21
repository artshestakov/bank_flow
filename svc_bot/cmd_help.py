from aiogram.types import Message

async def Help(msg: Message):
    await msg.answer("This is help")