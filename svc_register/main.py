import json
import psycopg2
import utils.db as db
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.route("/create", methods=["POST"])
def logout():
    params = json.loads(request.data)

    # Проверяем параметры запроса

    if "login" not in params:
        return Response(status=400, response="Поле 'login' отсутствует!")

    if "first_name" not in params:
        return Response(status=400, response="Поле 'first_name' отсутствует!")

    if "last_name" not in params:
        return Response(status=400, response="Поле 'last_name' отсутствует!")

    # Вытаскиваем параметры
    login = params["login"]
    first_name = params["first_name"]
    last_name = params["last_name"]

    # Убеждаемся, что они заполнены
    if len(login) == 0 or len(first_name) == 0 or len(last_name) == 0:
        return Response(status=400, response="Одно из полей пустое")

    conn = db.make_connect()

    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД")

    cur = conn.cursor()

    try:
        cur.execute(f"INSERT INTO customer(login, first_name, last_name) VALUES ('{login}', '{first_name}', '{last_name}')")
        conn.commit()
    except Exception as e:
        return Response(status=400, response=str(e))

    return Response(status=200, response="Регистрация прошла успешно")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
