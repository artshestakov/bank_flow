import requests
from aiogram.types import Message
from aiogram.enums import ParseMode

class AuthToken:
    def __init__(self):
        self.Value = str()

    Value: str

async def Login(msg: Message, auth_token: AuthToken):

    # Получаем токен
    try:
        r = requests.get(url="http://127.0.0.1:8000/login")
        response = r.json()
        auth_token.Value = response["token"]

        await msg.answer("Токен получен")
    except Exception as e:
        await msg.answer(str(e), parse_mode=ParseMode.MARKDOWN)


async def Logout(msg: Message, auth_token: AuthToken):

    try:
        data = {"token": auth_token.Value}
        r = requests.get(url="http://127.0.0.1:8000/logout", data=data)

        auth_token.Value = str()
        await msg.answer("Токен отдан")
    except Exception as e:
        await msg.answer(str(e), parse_mode=ParseMode.MARKDOWN)