import psycopg2
import utils.constants as c

def make_connect():

    try:
        return psycopg2.connect(host=c.DB_HOST,
                                port=c.DB_PORT,
                                dbname=c.DB_NAME,
                                user=c.DB_USER,
                                password=c.DB_PASS)

    except Exception as e:
        print(str(e))

    return None