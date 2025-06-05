import json
import random
import psycopg2
from decimal import Decimal
from flask import Flask, request, Response
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants, db, net, helper
# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
# ----------------------------------------------------------------------------------------------------------------------
@app.route("/create", methods=["GET"])
def create():

    data = net.ParseBody(request)
    if data is None:
        return Response(status=415, response="Не удалось разобрать тело запроса.")

    customer_id = data.get("customer_id")
    if customer_id is None:
        return Response(status=400, response="Поле 'customer_id' пустое!")

    conn = db.make_connect()
    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД.")

    cur = conn.cursor()
    number = int()

    while True:
        # Генерируем номер карты
        number = random.randint(1000000000000000, 9999999999999999)

        # Пытаемся вставить карту в БД
        try:

            cur.execute(f"INSERT INTO card(customer_id, number) VALUES ({customer_id}, {number})")
            conn.commit()
            break

        except psycopg2.DatabaseError as e:
            conn.rollback()

            match e.pgcode:

                # Такой номер карты уже есть - уходим на следующий круг
                case 23505:
                    continue

                # Нет такого пользователя в таблице customer
                case 23503:
                    return Response(400, "Нет такого пользователя.")

                # Все остальные случаи
                case _:
                    return Response(status=500, response=str(e))

    j = {
        "number": number
    }

    return Response(status=200, response=json.dumps(j))
# ----------------------------------------------------------------------------------------------------------------------
@app.route("/card_list", methods=["GET"])
def card_list():

    data = net.ParseBody(request)
    if data is None:
        return Response(status=415, response="Не удалось разобрать тело запроса.")

    customer_id = data.get("customer_id")
    if customer_id is None:
        return Response(status=400, response="Поле 'customer_id' пустое!")

    conn = db.make_connect()
    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД.")

    cur = conn.cursor()

    try:
        cur.execute(f"SELECT number FROM card WHERE customer_id = {customer_id} ORDER BY creation_date")
        rows = cur.fetchall()
        conn.commit()

        number_list = []

        # Формируем список карт пользователя
        for row in rows:
            number_list.append(row[0])

        return Response(status=200, response=json.dumps(number_list))

    except Exception as e:
        return Response(status=400, response=str(e))
# ----------------------------------------------------------------------------------------------------------------------
@app.route("/card", methods=["GET"])
def card():

    data = net.ParseBody(request)
    if data is None:
        return Response(status=415, response="Не удалось разобрать тело запроса.")

    number = data.get("number")
    if number is None:
        return Response(status=400, response="Поле 'number' пустое!")

    conn = db.make_connect()
    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД.")

    cur = conn.cursor()

    try:
        cur.execute(f"SELECT balance, TO_CHAR(creation_date, 'DD.MM.YYYY HH24:MI:SS') FROM card WHERE number = {number}")
        row = cur.fetchone()
        conn.commit()

        if row is None:
            return Response(status=404, response="Карта не найдена!")

        json_object = {
            "balance": row[0],
            "creation_date": row[1]
        }

        s = json.dumps(json_object, cls=helper.DecimalEncoder)
        return Response(status=200, response=s)

    except Exception as e:
        return Response(status=400, response=str(e))
# ----------------------------------------------------------------------------------------------------------------------
@app.route("/delete", methods=["DELETE"])
def delete():

    data = net.ParseBody(request)
    if data is None:
        return Response(status=415, response="Не удалось разобрать тело запроса.")

    number = data.get("number")
    if number is None:
        return Response(status=400, response="Поле 'number' пустое!")

    conn = db.make_connect()
    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД.")

    cur = conn.cursor()

    try:
        cur.execute(f"DELETE FROM card WHERE number = {number}")
        conn.commit()
    except Exception as e:
        return Response(status=400, response=str(e))

    return Response(status=200)
# ----------------------------------------------------------------------------------------------------------------------
@app.route("/deposit", methods=["PUT"])
def deposit():

    data = net.ParseBody(request)
    if data is None:
        return Response(status=415, response="Не удалось разобрать тело запроса.")

    number = data.get("number")
    if number is None:
        return Response(status=400, response="Поле 'number' пустое!")

    sum = data.get("sum")
    if sum is None:
        return Response(status=400, response="Поле 'sum' пустое!")

    conn = db.make_connect()
    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД.")

    cur = conn.cursor()
    balance_new = 0

    try:
        #number = 1
        cur.execute(f"UPDATE card SET balance = balance + {sum} WHERE number = {number} RETURNING balance")

        # Если ни одна запись не была обновлена - значит такой карты просто нет
        if cur.rowcount == 0:
            return Response(status=400, response=f"Карта {number} не найдена!")

        # Забираем новый баланс
        balance_new = cur.fetchone()[0]

        conn.commit()
    except Exception as e:
        return Response(status=400, response=str(e))

    return Response(status=200, response=f"Зачисление выполнено успешно\n\nБаланс: {balance_new}")
# ----------------------------------------------------------------------------------------------------------------------
def main():
    app.run(host='0.0.0.0', port=constants.TCP_PORT_CARD)
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ----------------------------------------------------------------------------------------------------------------------
