import json
import sys
import psycopg2
from flask import Flask, request, jsonify, Response
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants, db, net
# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
# ----------------------------------------------------------------------------------------------------------------------
@app.route("/create", methods=["POST"])
def create():

    data = net.ParseBody(request)
    if data is None:
        return Response(status=415, response="Не удалось разобрать тело запроса.")

    customer_id = data.get("customer_id")
    if customer_id is None:
        return Response(status=400, response="Поле 'customer_id' пустое!")

    first_name = data.get("first_name")
    if first_name is None:
        return Response(status=400, response="Поле 'first_name' пустое!")

    last_name = data.get("last_name")
    if last_name is None:
        return Response(status=400, response="Поле 'last_name' пустое!")

    conn = db.make_connect()
    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД")

    cur = conn.cursor()

    try:
        cur.execute(f"INSERT INTO customer(id, first_name, last_name) VALUES ('{customer_id}', '{first_name}', '{last_name}')")
        conn.commit()
    except Exception as e:
        return Response(status=400, response=str(e))

    return Response(status=200, response="Регистрация прошла успешно")
# ----------------------------------------------------------------------------------------------------------------------
@app.route("/get", methods=["GET"])
def get():

    data = net.ParseBody(request)
    if data is None:
        return Response(status=415, response="Не удалось разобрать тело запроса.")

    customer_id = data.get("customer_id")
    if customer_id is None:
        return Response(status=400, response="Поле 'customer_id' пустое!")

    conn = db.make_connect()

    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД")

    cur = conn.cursor()

    try:
        cur.execute(f"SELECT first_name, last_name FROM customer WHERE id = {customer_id}")
        customer = cur.fetchone()
        conn.commit()

        # Если запись не найдена - возвращаем 404
        if customer is None:
            return Response(status=404)

    except Exception as e:
        return Response(status=400, response=str(e))

    return Response(status=200)
# ----------------------------------------------------------------------------------------------------------------------
def main():
    app.run(host='0.0.0.0', port=constants.TCP_PORT_REGISTER)
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ----------------------------------------------------------------------------------------------------------------------
