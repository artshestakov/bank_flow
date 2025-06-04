import json
from flask import Flask, request, Response
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants, net, db, helper
# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
# ----------------------------------------------------------------------------------------------------------------------
@app.route("/create", methods=["POST"])
def card_list():

    data = net.ParseBody(request)
    if data is None:
        return Response(status=415, response="Не удалось разобрать тело запроса.")

    # Вытаскиваем параметры запроса

    # С какой карты будут списаны деньги
    card_from = data.get("card_from")
    if card_from is None:
        return Response(status=400, response="Поле 'card_from' пустое!")

    # На какую карту будут зачислены деньги
    card_to = data.get("card_to")
    if card_to is None:
        return Response(status=400, response="Поле 'card_to' пустое!")

    # Сумму
    sum = data.get("sum")
    if sum is None:
        return Response(status=400, response="Поле 'sum' пустое!")

    # Идём в сервис карт и проверяем карту-отправителя (с которой будут списаны деньги)
    q = net.NetQuery()
    q.Bind("number", card_from)
    status_code = q.execute_get(constants.TCP_PORT_CARD, "card")

    if status_code != 200:
        return Response(status=400, response=f"Карта {card_from} не найдена!")

    # Вытащим баланс карты-отправителя
    json_object_card = json.loads(q.m_Response)
    card_from_balance = json_object_card["balance"]

    # Если сумма транзакции превышает баланс карты-отправителя - запрещаем обслуживание
    if sum > card_from_balance:
        return Response(status=400, response="Недостаточно средств!")

    # Теперь проверим наличие карты-получателя (на которую будут зачислены деньги)
    q.Bind("number", card_to)
    status_code = q.execute_get(constants.TCP_PORT_CARD, "card")

    if status_code != 200:
        return Response(status=400, response=f"Карта {card_to} не найдена!")

    # Проверим, что карта-отправитель отличается от карты-получателя
    if card_from == card_to:
        return Response(status=400, response="Карта-отправитель и карта-получатель должны различаться!")

    conn = db.make_connect()
    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД.")

    cur = conn.cursor()

    # Идентификатор получателя уведомления о переводе (владелец карты-получателя)
    notify_customer_id = 0
    balance_new = 0

    # Выполним перевод средств с карты-отправителя на карту-получателя
    try:
        # Списываем средства с карты-отправителя
        cur.execute(f"UPDATE card SET balance = balance - {sum} WHERE number = {card_from}")

        # Зачисляем средства на карту-получателя
        cur.execute(f"UPDATE card SET balance = balance + {sum} WHERE number = {card_to} RETURNING customer_id, balance")
        r = cur.fetchone()
        notify_customer_id = r[0]
        balance_new = r[1]

        # Фиксируем транзакцию в БД
        cur.execute(f"INSERT INTO transaction(card_from, card_to, sum) VALUES({card_from}, {card_to}, {sum})")

        # Если дошли до этого момента - значит оба запроса прошли и можно сделать коммит транзакции
        conn.commit()

    except Exception as e:
        conn.rollback()
        return Response(status=400, response=f"Не удалось выполнить транзакцию: {str(e)}")

    if notify_customer_id != 0:
        q.Bind("customer_id", notify_customer_id)
        q.Bind("message",
               f"Зачисление средств\n\n"
               f"Карта: *{helper.short_card_number(card_to)}\n"
               f"Сумма: {sum}\n"
               f"Баланс: {balance_new}")
        q.execute_post(constants.TCP_PORT_NOTIFY, "notify")

    return Response(status=200)
# ----------------------------------------------------------------------------------------------------------------------
def main():
    app.run(host='0.0.0.0', port=constants.TCP_PORT_TRANSACTION)
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ----------------------------------------------------------------------------------------------------------------------
