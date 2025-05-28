import json
import sys
import uuid
from flask import Flask, request, jsonify, Response

sys.path.append("..")
from utils import constants

token_list = list()
app = Flask(__name__)

@app.route("/login", methods=['GET'])
def login():

    # Генерируем токен и вставляем его в список всех токенов
    token = str(uuid.uuid4())
    token = token.replace('-', '')
    token_list.append(token)

    return json.dumps({"token": token})

@app.route("/logout", methods=["POST"])
def logout(is_need_remove=True):
    # Парсим запрос
    params = json.loads(request.data)

    # Проверяем поля
    if "token" not in params:
        return Response(status=400, response="Поле с токеном отсутствует!")

    token = params["token"]

    if len(token) == 0:
        return Response(status=400, response="Токен пустой!")

    if token in token_list:
        if is_need_remove:
            token_list.remove(token)
    else:
        return Response(status=404, response="Токен не найден!")

    return Response(status=200, response="Выход выполнен!")


@app.route("/has", methods=["POST"])
def has():
    # Используем logout, чтобы не копипастить, но без удаления токена из памяти
    return logout(False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=constants.TCP_PORT_AUTH)
