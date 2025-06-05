import json
from decimal import Decimal
# ----------------------------------------------------------------------------------------------------------------------
def extract_digits_from_str(s: str):
    res = str()

    for char in s:
        if char.isdigit():
            res += char

    return res
# ----------------------------------------------------------------------------------------------------------------------
def short_card_number(number: int):
    return number % (10 ** 4)
# ----------------------------------------------------------------------------------------------------------------------
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)
# ----------------------------------------------------------------------------------------------------------------------
