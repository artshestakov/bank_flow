import json
from flask import Flask, request, Response
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants, net, db, helper
# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
# ----------------------------------------------------------------------------------------------------------------------
@app.route("/profile", methods=["GET"])
def profile():

    data = net.ParseBody(request)
    if data is None:
        return Response(status=415, response="Не удалось разобрать тело запроса.")

    # Кому будем отправлять уведомление
    customer_id = data.get("customer_id")
    if customer_id is None:
        return Response(status=400, response="Поле 'customer_id' пустое!")

    conn = db.make_connect()
    if conn is None:
        return Response(status=400, response="Не удалось подключиться к БД.")

    cur = conn.cursor()

    sql = f"""
        SELECT c.first_name, c.last_name,
        (
            SELECT COUNT(*) AS "card_count"
            FROM card c
            WHERE c.customer_id = {customer_id}
        ),
        (
            SELECT sum(c.balance) AS "total_balance"
            FROM card c
            WHERE c.customer_id = {customer_id}
        ),
        (
            SELECT COUNT(*) AS "transaction_count"
            FROM transaction t
            WHERE t.card_from IN (SELECT c.number FROM card c WHERE c.customer_id = {customer_id})
        )
        FROM customer c
        WHERE c.id = {customer_id}
    """

    # Вытаскиваем все данные по пользователю
    try:
        cur.execute(sql)
        row = cur.fetchone()

        # Если запись не найдена - значит такого пользователя нет
        if row is None:
            return Response(status=404, response="Пользователь не найден!")

        json_object = {
            "first_name": row[0],
            "last_name": row[1],
            "card_count": row[2],
            "total_balance": row[3],
            "transaction_count": row[4]
        }

        s = json.dumps(json_object, cls=helper.DecimalEncoder)
        return Response(status=200, response=s)

    except Exception as e:
        return Response(status=400, response=str(e))
# ----------------------------------------------------------------------------------------------------------------------
def main():
    app.run(host='0.0.0.0', port=constants.TCP_PORT_PROFILE)
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ----------------------------------------------------------------------------------------------------------------------
