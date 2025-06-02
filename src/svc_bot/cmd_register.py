from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants, net
# ----------------------------------------------------------------------------------------------------------------------
async def Register(context: CallbackContext, upd: Update):

    user = upd.callback_query.from_user

    # Идем в сервис регистрации и регистрируемся
    q = net.NetQuery()
    q.Bind("id", user.id)
    q.Bind("first_name", user.first_name)
    q.Bind("last_name", user.last_name)
    status_code = q.execute_post(constants.TCP_PORT_REGISTER, "create")

    keyboard = None

    # Если создание пользователя прошло успешно - предлагаем перейти в главное меню
    if status_code == 200:

        keyboard = [[InlineKeyboardButton("В главное меню", callback_data="main_menu")]]

        await context.bot.editMessageText(chat_id=user.id,
                                          message_id=upd.callback_query.message.message_id,
                                          text=q.m_Response,
                                          reply_markup=InlineKeyboardMarkup(keyboard))

    # Что-то пошло не так - предлагаем повторить
    else:
        await context.bot.editMessageText(chat_id=user.id,
                                          message_id=upd.callback_query.message.message_id,
                                          text=f"Что-то пошло не так: {q.m_Response}")
# ----------------------------------------------------------------------------------------------------------------------
async def RegisterCancel(context: CallbackContext, chat_id: int, message_id: int) -> None:
    # Удаляем сообщение из чата
    await context.bot.deleteMessage(chat_id=chat_id, message_id=message_id)
# ----------------------------------------------------------------------------------------------------------------------
