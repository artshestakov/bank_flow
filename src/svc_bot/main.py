import asyncio
import logging
import sys

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

#from os import getenv
#import aiogram.utils.formatting
#from aiogram import Bot, Dispatcher, html
#from aiogram import Dispatcher
#from aiogram.client.default import DefaultBotProperties
#from aiogram.enums import ParseMode
#from aiogram.filters import CommandStart
#from aiogram.types import Message, BotCommand



#import cmd_start
from src.svc_bot import cmd_start
#from src.svc_bot import cmd_register
#from src.svc_bot.cmd_auth import Login, Logout, AuthToken
#from src.svc_bot.cmd_card import CardCreate




#auth_token = AuthToken()

"""
# Класс описывающий команду
class CMD:
    Name: str
    args: list
"""

"""
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
"""

"""
@dp.message()
async def incoming_message(message: Message) -> None:

    # Конвертируем текст сообщения в команду
    cmd = make_command(message.text)

    # Если это не команда - выходим
    if cmd is None:
        return None

    match cmd.Name:
        case "/start":
            await cmd_start.Start(message)
        case "/register":
            await cmd_register.Register(message, cmd.args)
        case "/login":
            await Login(message, auth_token, cmd.args)
        case "/logout":
            await Logout(message, auth_token)
        case "/card_create":
            await CardCreate(message, auth_token.Value)
        case _:
            await message.answer("Такая команда не поддерживается.")
"""

"""
async def main() -> None:

    bot_commands = [
        BotCommand(command="/register", description="Регистрация (login, first_name, last_name)"),
        BotCommand(command="/login", description="Авторизация (login)"),
        BotCommand(command="/logout", description="Выход"),
        BotCommand(command="/card_create", description="Создание карты")
    ]

    bot = Bot(token="8116206559:AAEpY3NXGE1KzJTr9VXN0DhY-f66Yz1JEWk", default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands(bot_commands)

    await dp.start_polling(bot)
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await cmd_start.Start(update)
    #await update.message.reply_text("123")

def main() -> None:
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    #asyncio.run(main())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    bot = Application.builder().token("8116206559:AAEpY3NXGE1KzJTr9VXN0DhY-f66Yz1JEWk").build()
    bot.add_handler(CommandHandler("start", start))

    #bot.run_polling(allowed_updates=Update.ALL_TYPES)
    loop.run_until_complete(bot.run_polling(allowed_updates=Update.ALL_TYPES))

if __name__ == "__main__":
    main()
