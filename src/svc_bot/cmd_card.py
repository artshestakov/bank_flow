import json

import telegram.constants
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import net, constants, helper
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
async def CardList(upd: Update, context: CallbackContext):

    user = upd.callback_query.from_user

    q = net.NetQuery()
    q.Bind("customer_id", user.id)
    status_code = q.execute_get(constants.TCP_PORT_CARD, "card_list")

    if status_code != 200:
        await context.bot.send_message(chat_id=user.id,
                                       text=f"Что-то пошло не так: {q.m_Response}")
        return

    json_array = json.loads(q.m_Response)
    text = "*Мои карты:*\n\n"
    keyboard = []

    # Если карт нет - так и говорим
    if len(json_array) == 0:
        text += "В настоящий момент у вас нет ни одной карты. Нажмите кнопку *Новая карта* для добавления вашей первой карты."
    else:
        # Формируем клавиатуру с картами
        for number in json_array:

            short_number = number % (10 ** 4)

            tmp_list = []
            btn_card = InlineKeyboardButton(text=f"💳 *{short_number}", callback_data=f"card_click_{number}")
            tmp_list.append(btn_card)

            keyboard.append(tmp_list)

    keyboard.append([InlineKeyboardButton("➕ Новая карта", callback_data="card_create")])
    keyboard.append([InlineKeyboardButton("↩ Главное меню", callback_data="main_menu")])

    await context.bot.editMessageText(message_id=upd.callback_query.message.message_id,
                                      chat_id=user.id,
                                      parse_mode=telegram.constants.ParseMode.MARKDOWN,
                                      text=text,
                                      reply_markup=InlineKeyboardMarkup(keyboard))
# ----------------------------------------------------------------------------------------------------------------------
async def CardClick(upd: Update, context: CallbackContext):

    # Вытаскиваем номер карты
    card_number = upd.callback_query.data
    card_number = helper.extract_digits_from_str(card_number)

    q = net.NetQuery()
    q.Bind("number", card_number)
    status_code = q.execute_get(constants.TCP_PORT_CARD, "card")

    if status_code != 200:
        await context.bot.send_message(chat_id=upd.callback_query.from_user.id,
                                       text=f"Что-то пошло не так: {q.m_Response}")
        return

    json_object = json.loads(q.m_Response)

    text = "💳 *Карта*\n"
    text += f"`{str(card_number)}`\n\n"

    text += f"📅 *Дата заведения карты*\n"
    text += f"{json_object[1]}\n\n"

    balance = json_object[0]

    if int(balance) == 0:
        balance = str("0")

    text += f"💸 Баланс: {balance}"

    keyboard = [
        [
            InlineKeyboardButton("❌ Удалить", callback_data=f"card_delete_{card_number}")
        ],
        [
            InlineKeyboardButton("↩ К списку карт", callback_data="card_list")
        ]
    ]

    await context.bot.editMessageText(message_id=upd.callback_query.message.message_id,
                                      chat_id=upd.callback_query.from_user.id,
                                      parse_mode=telegram.constants.ParseMode.MARKDOWN,
                                      text=text,
                                      reply_markup=InlineKeyboardMarkup(keyboard))
# ----------------------------------------------------------------------------------------------------------------------
async def CardDelete(upd: Update, context: CallbackContext) -> bool:

    # Вытаскиваем номер карты
    card_number = upd.callback_query.data
    card_number = helper.extract_digits_from_str(card_number)

    # И идём в сервис карт с удалением
    q = net.NetQuery()
    q.Bind("number", card_number)
    status_code = q.execute_delete(constants.TCP_PORT_CARD, "delete")

    if status_code != 200:
        await context.bot.send_message(chat_id=upd.callback_query.from_user.id,
                                       text=f"Что-то пошло не так: {q.m_Response}")
        return False

    return True
# ----------------------------------------------------------------------------------------------------------------------
