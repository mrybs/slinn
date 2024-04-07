from slinn.http_json_response import HttpJSONResponse


class HttpJSONAPIResponse(HttpJSONResponse):
	def __init__(self, **payload: dict):
		super().__init__(payload)
		default_data = [('Server', 'Slinn'), ('Content-Type', self.content_type), ('Access-Control-Allow-Origin', '*')]
		self.data = default_data + self.data if self.data is not None else default_data
