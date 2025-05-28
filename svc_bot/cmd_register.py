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

async def Register(msg: Message, params: list):

    if len(params) != 3:
        return

    data = {
        "login": params[0],
        "first_name": params[1],
        "last_name": params[2]
    }

    try:
        r = requests.post(url=f"http://127.0.0.1:{constants.TCP_PORT_REGISTER}/create", json=data)
        await msg.answer(r.text)
    except Exception as e:
        await msg.answer(str(e), parse_mode=ParseMode.MARKDOWN)
