import json
import uuid

from flask import Flask, request, jsonify

token_list = list()
app = Flask(__name__)

@app.route('/auth', methods=['GET'])
def auth():

    # Генерируем токен и вставльяем его в список всех токенов
    token = str(uuid.uuid4())
    token_list.append(token)

    return json.dumps({"token": token})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
