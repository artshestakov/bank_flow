import json
# ----------------------------------------------------------------------------------------------------------------------
from telegram import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants, net
# ----------------------------------------------------------------------------------------------------------------------
async def Profile(msg: Message, context: CallbackContext) -> None:

    customer_id = msg.chat.id

    # Идем в сервис профилей и забираем информацию по клиенту
    q = net.NetQuery()
    q.Bind("customer_id", customer_id)
    status_code = q.execute_get(constants.TCP_PORT_PROFILE, "profile")

    # Если что-то пошло не так
    if status_code != 200:
        await context.bot.send_message(chat_id=customer_id, text=q.m_Response)
        return

    json_object = json.loads(q.m_Response)

    text = "👤 Мой профиль\n\n"
    text += f"Фамилия: {json_object['first_name']}\n"
    text += f"Имя: {json_object['last_name']}\n"
    text += f"Карты: {json_object['card_count']}\n"
    text += f"Общий баланс: {json_object['total_balance']}\n"
    text += f"Транзакции: {json_object['transaction_count']}"

    keyboard = [
        [
            InlineKeyboardButton("↩ В главное меню", callback_data="main_menu")
        ]
    ]

    await context.bot.editMessageText(chat_id=customer_id,
                                      message_id=msg.message_id,
                                      text=text,
                                      reply_markup=InlineKeyboardMarkup(keyboard))
# ----------------------------------------------------------------------------------------------------------------------
