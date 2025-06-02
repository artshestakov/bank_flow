import json
import sys
import random
import psycopg2
from flask import Flask, request, Response
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants, db, net
# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
# ----------------------------------------------------------------------------------------------------------------------
@app.route("/create", methods=["GET"])
def create():

    data = net.ParseBody(request)
    if data is None:
        return Response(status=415, response="Не удалось разобрать тело запроса.")

    customer_id = data.get("customer_id")

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
def main():
    app.run(host='0.0.0.0', port=constants.TCP_PORT_CARD)
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ----------------------------------------------------------------------------------------------------------------------
