import json

import typing
from fastapi.responses import JSONResponse

from .encoders import ResponseEncoder


class JsonResponse(JSONResponse):

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            cls=ResponseEncoder,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
