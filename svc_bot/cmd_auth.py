import requests
from aiogram.types import Message
from aiogram.enums import ParseMode

class AuthToken:
    Value: str

async def Auth(msg: Message, auth_token: AuthToken):

    # Получаем токен
    try:
        r = requests.get(url="http://127.0.0.1:8000/auth")
        response = r.json()
        auth_token.Value = response["token"]

        await msg.answer("Авторизация пройдена успешно!")
    except Exception as e:
        await msg.answer(str(e), parse_mode=ParseMode.MARKDOWN)
