import json
import uuid

from flask import Flask, request, jsonify, Response

token_list = list()
app = Flask(__name__)

@app.route("/login", methods=['GET'])
def login():

    # Генерируем токен и вставльяем его в список всех токенов
    token = str(uuid.uuid4())
    token = token.replace('-', '')
    token_list.append(token)

    return json.dumps({"token": token})

@app.route("/logout", methods=["GET"])
def logout():
    # Парсим запрос
    params = json.loads(request.data)

    # Проверяем поля
    if "token" not in params:
        return Response(status=400, response="Field 'token' does not exist")

    token = params["token"]

    if len(token) == 0:
        return Response(status=400, response="Token is empty")

    if token in token_list:
        token_list.remove(token)
    else:
        return Response(status=404, response="Token not found")

    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
