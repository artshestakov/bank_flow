import requests
from flask import Flask, request, Response
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants, net
# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
# ----------------------------------------------------------------------------------------------------------------------
@app.route("/notify", methods=["POST"])
def notify():
    net.Audit(__file__, sys._getframe().f_code.co_name)

    data = net.ParseBody(request)
    if data is None:
        return Response(status=415, response="Не удалось разобрать тело запроса.")

    # Кому будем отправлять уведомление
    customer_id = data.get("customer_id")
    if customer_id is None:
        return Response(status=400, response="Поле 'customer_id' пустое!")

    # Текст уведомления
    message = data.get("message")
    if message is None:
        return Response(status=400, response="Поле 'message' пустое!")

    # Отправляем уведомление
    try:
        url = f"https://api.telegram.org/bot{constants.BOT_TOKEN}/sendMessage?chat_id={customer_id}&text={message}"
        r = requests.get(url)
    except Exception as e:
        return Response(status=400, response=str(e))

    return Response(status=200)
# ----------------------------------------------------------------------------------------------------------------------
def main():
    app.run(host='0.0.0.0', port=constants.TCP_PORT_NOTIFY)
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ----------------------------------------------------------------------------------------------------------------------
