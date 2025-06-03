import json
import sys
import random
import psycopg2
from decimal import Decimal
from flask import Flask, request, Response
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants, db, net
# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
# ----------------------------------------------------------------------------------------------------------------------
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Или str(obj) для точного представления
        return super().default(obj)
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
def main():
    app.run(host='0.0.0.0', port=constants.TCP_PORT_CARD)
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ----------------------------------------------------------------------------------------------------------------------
