import sys
import requests
from aiogram.types import Message
from aiogram.enums import ParseMode

sys.path.append("..")
from utils import constants

class AuthToken:
    def __init__(self):
        self.Value = str()

    Value: str

async def Login(msg: Message, auth_token: AuthToken, params: list):

    data = {
        "login": params[0]
    }

    # Получаем токен
    try:
        r = requests.post(url=f"http://127.0.0.1:{constants.TCP_PORT_AUTH}/login", json=data)
        response = r.json()
        auth_token.Value = response["token"]

        await msg.answer("Токен получен")
    except Exception as e:
        await msg.answer(str(e), parse_mode=ParseMode.MARKDOWN)


async def Logout(msg: Message, auth_token: AuthToken):

    try:
        r = requests.post(url=f"http://127.0.0.1:{constants.TCP_PORT_AUTH}/logout", json={"token": auth_token.Value})
        await msg.answer(r.text)

        auth_token.Value = str()

    except Exception as e:
        await msg.answer(str(e), parse_mode=ParseMode.MARKDOWN)