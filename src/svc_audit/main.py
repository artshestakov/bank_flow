from flask import Flask, request, Response
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants, net, db
# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
# ----------------------------------------------------------------------------------------------------------------------
@app.route("/create", methods=["POST"])
def create():

    data = net.ParseBody(request)
    if data is None:
        return Response(status=415, response="Не удалось разобрать тело запроса.")

    # Сервис-источник
    service_source = data.get("service_source")
    if service_source is None:
        return Response(status=400, response="Поле 'service_source' пустое!")

    # Сообщение
    message = data.get("message")
    if message is None:
        return Response(status=400, response="Поле 'message' пустое!")

    conn = db.make_connect()
    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД.")

    cur = conn.cursor()

    try:
        cur.execute(f"INSERT INTO audit(service_source, message) VALUES('{service_source}', '{message}')")
        conn.commit()
    except Exception as e:
        print(message)
        print(str(e))

    # Да да, мы всегда отдаём 200, чтобы не накручивать логику в вызывающем сервисе
    # Нам достаточно логирования в консоль при возникновении исключения выше
    return Response(status=200)
# ----------------------------------------------------------------------------------------------------------------------
def main():
    app.run(host='0.0.0.0', port=constants.TCP_PORT_AUDIT)
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ----------------------------------------------------------------------------------------------------------------------
