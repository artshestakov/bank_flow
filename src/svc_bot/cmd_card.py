import json

import telegram.constants
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import net, constants
# ----------------------------------------------------------------------------------------------------------------------
async def CardCreate(upd: Update, context: CallbackContext) -> bool:

    user = upd.callback_query.from_user

    # Идем в сервис карт и просим создать новую карту
    q = net.NetQuery()
    q.Bind("customer_id", user.id)
    status_code = q.execute_get(constants.TCP_PORT_CARD, "create")

    if status_code != 200:
        await context.bot.send_message(chat_id=user.id,
                                       text=f"Что-то пошло не так: {q.m_Response}")

    return status_code == 200
# ----------------------------------------------------------------------------------------------------------------------
async def CardList(upd: Update, context: CallbackContext, parent_message_id: int):

    user = upd.callback_query.from_user

    q = net.NetQuery()
    q.Bind("customer_id", user.id)
    status_code = q.execute_get(constants.TCP_PORT_CARD, "card_list")

    if status_code != 200:
        await context.bot.send_message(chat_id=user.id,
                                       text=f"Что-то пошло не так: {q.m_Response}")

    json_array = json.loads(q.m_Response)
    text = "*Мои карты:*\n\n"

    # Если карт нет - так и говорим
    if len(json_array) == 0:
        text += "В настоящий момент у вас нет ни одной карты. Нажмите кнопку *Создать* для добавления вашей первой карты."
    else:
        # Формируем клавиатуру с картами
        for json_object in json_array:
            number = str(json_object[0])
            balance = str(json_object[1])
            date_time = str(json_object[2])

            text += f"💳 `{number}`\n💸 {balance}\n📅 {date_time}\n\n"

    keyboard = [
        [
            InlineKeyboardButton("🔄 Обновить", callback_data="card_list_update"),
            InlineKeyboardButton("➕ Создать", callback_data="card_create")
        ]
    ]

    await context.bot.editMessageText(message_id=upd.callback_query.message.message_id,
                                      chat_id=user.id,
                                      parse_mode=telegram.constants.ParseMode.MARKDOWN,
                                      text=text,
                                      reply_markup=InlineKeyboardMarkup(keyboard))
# ----------------------------------------------------------------------------------------------------------------------
