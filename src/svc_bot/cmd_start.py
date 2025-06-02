from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, User
from telegram.ext import CallbackContext
from src.utils import constants, net
# ----------------------------------------------------------------------------------------------------------------------
async def Start(user: User, context: CallbackContext, parent_message_id=None) -> None:
    # Идем в сервис регистрации и спрашиваем, есть ли такой пользователь
    q = net.NetQuery()
    q.Bind("id", user.id)
    status_code = q.execute_get(constants.TCP_PORT_REGISTER, "get")

    # Если что-то пошло не так
    if status_code is None:
        await context.bot.send_message(chat_id=user.id, text=q.m_Response)

    msg_title = str()
    keyboard = None

    # Если пользователь найден - отдаём главное меню
    if status_code == 200:

        msg_title = "🔹 Главное меню 🔹"
        keyboard = [
            [
                InlineKeyboardButton("👤 Мой профиль", callback_data="register_profile")
            ]
        ]

    # Пользователя нет - предлагаем зарегистрироваться
    elif status_code == 404:

        msg_title = "Ваша учётная запись не найдена. Вы хотите зарегистрироваться?"
        keyboard = [
            [
                InlineKeyboardButton("✅ Да", callback_data="register_yes"),
                InlineKeyboardButton("❌ Нет", callback_data="register_no")
            ]
        ]

    # Если родительного сообщения нет - отправляем новое сообшение
    if parent_message_id is None:
        await context.bot.send_message(chat_id=user.id,
                                       text=msg_title,
                                       reply_markup=InlineKeyboardMarkup(keyboard))
    else: # В ином случае меняем указанное
        await context.bot.editMessageText(message_id=parent_message_id,
                                          chat_id=user.id,
                                          text=msg_title,
                                          reply_markup=InlineKeyboardMarkup(keyboard))
# ----------------------------------------------------------------------------------------------------------------------
