import sys
import requests
from aiogram.types import Message
from aiogram.enums import ParseMode

sys.path.append("..")
from utils import constants
from utils import net


async def CardCreate(msg: Message, token: str):

    if net.validate_token(token):
        await msg.answer("Неверный токен")

    #if len(params) != 3:
    #    return

    headers = {
        "token": token
    }

    try:
        r = requests.post(url=f"http://127.0.0.1:{constants.TCP_PORT_CARD}/create", headers=headers)
        await msg.answer(r.text)
    except Exception as e:
        await msg.answer(str(e), parse_mode=ParseMode.MARKDOWN)
        return
