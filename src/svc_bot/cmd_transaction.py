from telegram import Message
from telegram.ext import CallbackContext
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants, net
# ----------------------------------------------------------------------------------------------------------------------
async def Transaction(msg: Message, context: CallbackContext) -> None:

    if len(context.args) != 3:
        await context.bot.send_message(chat_id=msg.from_user.id,
                                       text="Некорректная команда!")
        return

    card_from = context.args[0]

    try:
        card_from = int(card_from)
    except ValueError as e:
        await context.bot.send_message(chat_id=msg.from_user.id,
                                       text=f"Значение '{card_from}' не является числом!")
        return

    card_to = context.args[1]

    try:
        card_to = int(card_to)
    except ValueError as e:
        await context.bot.send_message(chat_id=msg.from_user.id,
                                       text=f"Значение '{card_to}' не является числом!")
        return

    sum = context.args[2]

    try:
        sum = float(sum)
    except ValueError as e:
        await context.bot.send_message(chat_id=msg.from_user.id,
                                       text=f"Значение '{sum}' не является числом!")
        return

    # Идем в сервис транзакций и просим выполнить транзакцию
    q = net.NetQuery()
    q.Bind("card_from", card_from)
    q.Bind("card_to", card_to)
    q.Bind("sum", sum)
    status_code = q.execute_post(constants.TCP_PORT_TRANSACTION, "create")

    # Если что-то пошло не так
    if status_code != 200:
        await context.bot.send_message(chat_id=msg.from_user.id, text=q.m_Response)
        return

    # Транзакция прошла успешно - информируем пользователя
    await context.bot.send_message(chat_id=msg.from_user.id,
                                   text=f"Транзакция выполнена успешно!",
                                   reply_to_message_id=msg.message_id)
# ----------------------------------------------------------------------------------------------------------------------
