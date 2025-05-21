from aiogram.types import Message

async def Help(msg: Message):

    await msg.answer("""
/start - приветственное сообщение
/help - список всех команд
/auth - авторизация
    """)
