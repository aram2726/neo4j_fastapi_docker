from typing import TypedDict

CONDITIONS = ("eq", "ne", "gt", "gte", "lt", "lte")
CONDITIONS_MAP = {
    "eq": "=",
    "ne": "!=",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<="
}


class Condition(TypedDict):
    key: str
    condition: str
    value: str


class BaseFilter:
    def generate(self, condition: Condition):
        return f""
