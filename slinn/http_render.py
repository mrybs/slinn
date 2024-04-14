from slinn.http_response import HttpResponse

class HttpRender(HttpResponse):
	def __init__(self, file_path: str, data: list[tuple]=None,status: str='200 OK'):
		self.file_path = file_path
		self.file_extension = file_path.split('.')[-1]
		self.data = data
		self.status = status

	def make(self):
		match self.file_extension:
			case 'html':
				with open(self.file_path, 'r') as f:
					self.payload = f.read()
					self.content_type = 'text/html'
			case 'css':
				with open(self.file_path, 'r') as f:
					self.payload = f.read()
					self.content_type = 'text/css'
			case 'js':
				with open(self.file_path, 'r') as f:
					self.payload = f.read()
					self.content_type = 'text/javascript'
			case 'png':
				with open(self.file_path, 'rb') as f:
					self.payload = f.read()
					self.content_type = 'image/png'
			case 'jpg':
				with open(self.file_path, 'rb') as f:
					self.payload = f.read()
					self.content_type = 'image/jpg'
			case 'svg':
				with open(self.file_path, 'rb') as f:
					self.payload = f.read()
					self.content_type = 'image/svg'
		self.data = self.data if self.data is not None else [('Content-Type', self.content_type), ('Server', 'Slinn')] + ([] if type(self.payload) in [str, int, float, bool, dict] else [('Content-Length', len(self.payload))])
		return super().make()