from slinn.http_response import HttpResponse
import json


class HttpJSONResponse(HttpResponse):
	def __init__(self, **payload: dict):
		data = payload['data'] if 'data' in payload.keys() else None
		status = payload['status'] if 'status' in payload.keys() else '200 OK'
		content_type = payload['content_type'] if 'content_type' in payload.keys() else 'text/plain'
		super().__init__(payload=json.dumps(payload), data=data, status=status, content_type=content_type)