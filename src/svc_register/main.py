import json
import sys
import psycopg2
from flask import Flask, request, jsonify, Response

sys.path.append("..")
from utils import db, constants

app = Flask(__name__)

@app.route("/create", methods=["POST"])
def create():
    params = json.loads(request.data)

    # Проверяем параметры запроса

    if "id" not in params:
        return Response(status=400, response="Поле 'id' отсутствует!")

    if "first_name" not in params:
        return Response(status=400, response="Поле 'first_name' отсутствует!")

    if "last_name" not in params:
        return Response(status=400, response="Поле 'last_name' отсутствует!")

    # Вытаскиваем параметры
    id = params["id"]
    first_name = params["first_name"]
    last_name = params["last_name"]

    # Убеждаемся, что они заполнены
    if len(id) == 0 or len(first_name) == 0 or len(last_name) == 0:
        return Response(status=400, response="Одно из полей пустое")

    conn = db.make_connect()

    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД")

    cur = conn.cursor()

    try:
        cur.execute(f"INSERT INTO customer(id, first_name, last_name) VALUES ('{id}', '{first_name}', '{last_name}')")
        conn.commit()
    except Exception as e:
        return Response(status=400, response=str(e))

    return Response(status=200, response="Регистрация прошла успешно")


@app.route("/get", methods=["GET"])
def get():
    params = json.loads(request.data)

    if "id" not in params:
        return Response(status=400, response="Поле 'id' отсутствует!")

    id = params["id"]

    conn = db.make_connect()

    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД")

    cur = conn.cursor()

    try:
        cur.execute(f"SELECT first_name, last_name FROM customer WHERE id = {id}")
        a = cur.fetchone()
        conn.commit()

        # Если запись не найдена - возвращаем 404
        if a is None:
            return Response(status=404)

    except Exception as e:
        return Response(status=400, response=str(e))

    return Response(status=200)


def main():
    app.run(host='0.0.0.0', port=constants.TCP_PORT_REGISTER)


if __name__ == '__main__':
    main()
