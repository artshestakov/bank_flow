import json
import requests
import os
from enum import Enum
# ----------------------------------------------------------------------------------------------------------------------
from src.utils import constants
# ----------------------------------------------------------------------------------------------------------------------
class MethodType(Enum):
    GET = 1,
    POST = 2,
    DELETE = 3,
    PUT = 4
# ----------------------------------------------------------------------------------------------------------------------
class NetQuery:
    def __init__(self):
        self.m_Params = {}
        self.m_Response = str()

    def Bind(self, param_name: str, param_value: str) -> None:
        self.m_Params[param_name] = param_value

    def execute_get(self, port: int, method: str) -> int:
        return self.execute(MethodType.GET, port, method)

    def execute_post(self, port: int, method: str) -> int:
        return self.execute(MethodType.POST, port, method)

    def execute_delete(self, port: int, method: str) -> int:
        return self.execute(MethodType.DELETE, port, method)

    def execute_put(self, port: int, method: str) -> int:
        return self.execute(MethodType.PUT, port, method)

    def execute(self, method_type: MethodType, port: int, method_name: str) -> int:

        url = f"http://127.0.0.1:{port}/{method_name}"
        json_body = json.dumps(self.m_Params)
        headers = {"Content-Type": "application/json"}
        response = None

        try:

            match method_type:
                case MethodType.GET:
                    response = requests.get(url, data=json_body, headers=headers)
                case MethodType.POST:
                    response = requests.post(url, data=json_body, headers=headers)
                case MethodType.DELETE:
                    response = requests.delete(url, data=json_body, headers=headers)
                case MethodType.PUT:
                    response = requests.put(url, data=json_body, headers=headers)

            self.m_Response = response.text
            return response.status_code

        except Exception as e:
            self.m_Response = f"Не удалось выполнить запрос: {str(e)}"

        self.m_Params.clear()

        return None
# ----------------------------------------------------------------------------------------------------------------------
def ParseBody(request: requests.Request) -> dict:
    try:
        return request.get_json()
    except Exception as e:
        print(f"Failed to convert request body to json: {str(e)}")

    return None
# ----------------------------------------------------------------------------------------------------------------------
def Audit(script_path: str, msg: str) -> None:

    script_dir = os.path.dirname(os.path.abspath(script_path))
    script_dir = os.path.basename(script_dir)

    q = NetQuery()
    q.Bind("service_source", script_dir)
    q.Bind("message", msg)
    q.execute_post(constants.TCP_PORT_AUDIT, "create")
# ----------------------------------------------------------------------------------------------------------------------
