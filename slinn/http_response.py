class HttpResponse:
	def __init__(self, payload: any, data: list[tuple]=None, status: str='200 OK', content_type: str='text/plain'):
		self.payload = str(payload).encode() if type(payload) in [str, int, float, bool, dict] else bytes(payload)
		self.data = data if data is not None else [('Content-Type', content_type), ('Server', 'Slinn')] + ([] if type(payload) in [str, int, float, bool, dict] else [('Content-Length', len(self.payload))])
		self.status = status
	
	def set_cookie(self, key: str, value: any):
		self.data.append(('Set-Cookie', f'{key}={value}'))
	
	def make(self, type: str='HTTP/2.0') -> str:
		return (f'{type} {self.status}'+'\r\n'+"\r\n".join([str(dat[0])+": "+str(dat[1]) for dat in self.data])+'\r\n\r\n').encode()+self.payload