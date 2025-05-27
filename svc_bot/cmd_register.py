import requests
from aiogram.types import Message
from aiogram.enums import ParseMode

class AuthToken:
    def __init__(self):
        self.Value = str()

    Value: str

async def Register(msg: Message, params: list):

    if len(params) != 3:
        return

    user_name = params[0]
    first_name = params[1]
    last_name = params[2]
