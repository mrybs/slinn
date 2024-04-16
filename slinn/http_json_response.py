from slinn.http_response import HttpResponse
import json


class HttpJSONResponse(HttpResponse):
    def __init__(self, **payload: dict | list[dict]) -> None:
        self.data = payload['__data'] if '__data' in payload.keys() else None
        self.status = payload['__status'] if '__status' in payload.keys() else '200 OK'
        self.content_type = 'application/json'
        del payload['__data']
        del payload['__status']
        del payload['__content_type']
        super().__init__(payload=json.dumps(payload) if type(
            payload) is dict else f'[{", ".join([json.dumps(i) for i in payload])}]', data=self.data,
                         status=self.status, content_type=self.content_type)
