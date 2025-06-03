import psycopg2
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants
# ----------------------------------------------------------------------------------------------------------------------
def make_connect():

    try:
        return psycopg2.connect(host=constants.DB_HOST,
                                port=constants.DB_PORT,
                                dbname=constants.DB_NAME,
                                user=constants.DB_USER,
                                password=constants.DB_PASS)

    except Exception as e:
        print(str(e))

    return None
# ----------------------------------------------------------------------------------------------------------------------
