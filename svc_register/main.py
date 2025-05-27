import json
import uuid

from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.route("/create", methods=["POST"])
def logout():
    params = json.loads(request.data)

    if "user_name" not in params:
        return Response(status=400, response="Поле 'user_name' отсутствует!")

    if "first_name" not in params:
        return Response(status=400, response="Поле 'first_name' отсутствует!")

    if "last_name" not in params:
        return Response(status=400, response="Поле 'last_name' отсутствует!")

    user_name = params["user_name"]
    first_name = params["first_name"]
    last_name = params["last_name"]

    if len(user_name) == 0 or len(first_name) == 0 or len(last_name) == 0:
        return Response(status=400, response="Одно из полей пустое")

    return Response(status=200, response="Регистрация прошла успешно")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
