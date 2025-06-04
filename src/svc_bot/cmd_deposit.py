from telegram import Message
from telegram.ext import CallbackContext
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants, net
# ----------------------------------------------------------------------------------------------------------------------
async def Deposit(msg: Message, context: CallbackContext) -> None:

    if len(context.args) != 2:
        await context.bot.send_message(chat_id=msg.from_user.id,
                                       text="Некорректная команда!")
        return

    cardnum = context.args[0]

    try:
        cardnum = int(cardnum)
    except ValueError as e:
        await context.bot.send_message(chat_id=msg.from_user.id,
                                       text=f"Значение '{cardnum}' не является числом!")
        return

    sum = context.args[1]

    try:
        sum = float(sum)
    except ValueError as e:
        await context.bot.send_message(chat_id=msg.from_user.id,
                                       text=f"Значение '{sum}' не является числом!")
        return

    # Идем в сервис карт и просим положить деньги на карту
    q = net.NetQuery()
    q.Bind("number", cardnum)
    q.Bind("sum", sum)
    status_code = q.execute_put(constants.TCP_PORT_CARD, "deposit")

    # Если что-то пошло не так
    if status_code != 200:
        await context.bot.send_message(chat_id=msg.from_user.id, text=q.m_Response)
        return

    # Поплнение выполнено успешно
    await context.bot.send_message(chat_id=msg.from_user.id, text=q.m_Response)
# ----------------------------------------------------------------------------------------------------------------------
