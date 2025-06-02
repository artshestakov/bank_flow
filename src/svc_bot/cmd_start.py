from telegram import Update
from src.utils import constants, net

async def Start(upd: Update):

    # Идем в сервис регистрации и спрашиваем, есть ли такой пользователь
    q = net.NetQuery()
    q.Bind("id", upd.message.from_user.id)
    status_code = q.execute_get(constants.TCP_PORT_REGISTER, "get")

    match status_code:
        case 200: # Пользователь найден - отдаём главное меню
            await upd.message.reply_text("Главное меню")
        case 404: # Пользователя нет - предлагаем зарегистрироваться
            await upd.message.reply_text("Регистрация")
        case _: # Что-то пошло не так
            await upd.message.reply_text(q.m_Response)
