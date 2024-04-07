import urllib.parse
from slinn import File

class Request:	
	RESET = '\u001b[0m'
	GRAY = '\u001b[38;2;127;127;127m'

	@staticmethod
	def parse_http_header(http_header: str):
		result = {}
		for line in http_header.split('\r\n'):
			key, value = line.split(':')[0], ':'.join(line.split(':')[1:])
			result[key.strip()] = value.strip()
		return result
	
	@staticmethod
	def parse_http_body(http_body: bytes):
		files = [File()]
		BGNs = [b'-----------------------------', b'------WebKitFormBoundary']
		END = b'--'
		binary = 0
		for line in http_body.split(b'\r\n'):
			if binary != 2:
				if line == b'':
					binary += 1
				elif b':' in line:
					key, value = line.split(b':')[0].decode(), b':'.join(line.split(b':')[1:])
					files[-1].header[key.strip()] = value.strip()
				elif files[-1].id is None:
					if line.startswith(BGNs[0]):
						files[-1].id = line[len(BGNs[0]):]
					elif line.startswith(BGNs[1]):
						files[-1].id = line[len(BGNs[1]):]
				continue
			if files[-1].id is not None:
				if line.startswith(BGNs[0]) and line.endswith(END) and line[len(BGNs[0]):-len(END)] == files[-1].id \
				   or line.startswith(BGNs[1]) and line.endswith(END) and line[len(BGNs[1]):-len(END)] == files[-1].id:
					files[-1].data = bytes(files[-1].data[:-2])
					files.append(File())
					binary = 0
					continue
			files[-1].data += line + b'\r\n'
		return files[:-1]

	def __init__(self, header: str, body: bytes, client_address: tuple[str, int]):
		def get_args(text):
				return {} if text == '' else {pair.split('=')[0]: '='.join(pair.split('=')[1:]) for pair in text.split('&')}
		
		self.type = header.split('\r\n')[0].strip().split(' ')
		self.header = {'method': self.type[0], 'link': ' '.join(self.type[1:-1]), 'ver': self.type[-1], 'data': {'user-agent': '', 'Accept': '', 'Accept-Encoding': '', 'Accept-Language': ''}}
		header = self.parse_http_header(header)
		self.files = self.parse_http_body(body)
		self.header['data'].update(header)
		self.ip, self.port = client_address[:2]
		self.method = self.header['method']
		self.version = self.header["ver"]
		self.full_link = urllib.parse.unquote_plus(self.header["link"].replace('+', ' '))
		self.host = self.header["data"]["Host"]
		self.user_agent = self.header["data"]["User-Agent"] if 'User-Agent' in self.header['data'].keys() else self.header['data']['user-agent']
		self.accept = self.header["data"]["Accept"].split(',')
		self.encoding = self.header["data"]["Accept-Encoding"].split(',')
		self.language = self.header["data"]["Accept-Language"].split(',')
		self.link = self.full_link[:(self.full_link.index('?') if '?' in self.full_link else None)]
		self.args = get_args(self.full_link[(self.full_link.index('?')+1 if '?' in self.full_link else len(self.full_link)):])
		self.cookies = {c.split('=')[0]:c.split('=')[1] for c in self.header["data"]["Cookie"].split(';')} if 'Cookie' in self.header['data'] else []

	def __str__(self):
		return f'{self.GRAY}[{self.method}]{self.RESET} request {self.full_link} from {"" if "." in self.ip else "["}{self.ip}{"" if "." in self.ip else "]"}:{self.port} on {self.host}'
