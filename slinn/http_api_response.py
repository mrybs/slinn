from slinn.http_response import HttpResponse


class HttpAPIResponse(HttpResponse):
	def __init__(self, payload: any, data: list[tuple]=None, status: str='200 OK', content_type: str='text/plain'):
		self.payload = str(payload).encode() if type(payload) in [str, int, float, bool, dict] else bytes(payload)
		default_data = [('Server', 'Slinn'), ('Content-Type', content_type), ('Access-Control-Allow-Origin', '*')]
		self.data = default_data + data if data is not None else default_data + ([] if type(payload) in [str, int, float, bool, dict] else [('Content-Length', len(self.payload))])
		self.status = status
