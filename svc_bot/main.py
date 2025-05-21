import asyncio
import logging
import sys
from os import getenv

import aiogram.utils.formatting
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from cmd_start import Start
from cmd_help import Help

TOKEN = "8116206559:AAEpY3NXGE1KzJTr9VXN0DhY-f66Yz1JEWk"
dp = Dispatcher()

# Класс описывающий команду
class CMD:
    Name: str
    args: list

def make_command(text: str):
    lst = text.split()
    cmd_name = lst[0]

    # Если это не команда - выходим
    if not cmd_name.startswith('/'):
        return None

    lst.pop(0)

    # Формируем объект команды
    cmd = CMD()
    cmd.Name = cmd_name
    cmd.args = lst

    return cmd

@dp.message()
async def incoming_message(message: Message) -> None:

    # Конвертируем текст сообщения в команду
    cmd = make_command(message.text)

    # Если это не команда - выходим
    if cmd is None:
        return None

    try:
        match cmd.Name:
            case "/start":
                await Start(message)
            case "/help":
                await Help(message)

    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
