from aiogram.types import Message

async def Start(msg: Message):
    await msg.answer("Добро пожаловать в бота")
