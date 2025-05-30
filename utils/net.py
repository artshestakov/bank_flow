import requests
from . import constants


def validate_token(token: str) -> bool:

    t = {
        "token": token
    }

    try:
        r = requests.post(f"http://127.0.0.1:{constants.TCP_PORT_AUTH}/has", json=t)
        if r.status_code == 200:
            return True

    except Exception as e:
        print(str(e))

    return False