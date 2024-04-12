from slinn.http_response import HttpResponse
import json


class HttpJSONResponse(HttpResponse):
	def __init__(self, **payload: dict):
		self.data = payload['data'] if 'data' in payload.keys() else None
		self.status = payload['status'] if 'status' in payload.keys() else '200 OK'
		self.content_type = payload['content_type'] if 'content_type' in payload.keys() else 'text/plain'
		super().__init__(payload=json.dumps(payload), data=self.data, status=self.status, content_type=self.content_type)
