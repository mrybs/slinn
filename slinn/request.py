import urllib.parse

class Request:	
	@staticmethod
	def parse_http_header(http_header: str):
		result = {}
		for line in http_header.split('\r\n'):
			key, value = line.split(':')[0], ':'.join(line.split(':')[1:])
			result[key.strip()] = value.strip()
		return result
	
	@staticmethod
	def parse_http_content(http_content: bytes):
		open('content.bin', 'wb').write(http_content)
		files = [{'data': bytearray()}]
		BGNs = [b'-----------------------------', b'------WebKitFormBoundary']
		END = b'--'
		binary = 0
		for line in http_content.split(b'\r\n'):
			if binary != 2:
				if line == b'':
					binary += 1
				elif b':' in line:
					key, value = line.split(b':')[0].decode(), b':'.join(line.split(b':')[1:])
					files[-1][key.strip()] = value.strip()
				elif 'id' not in files[-1].keys():
					if line.startswith(BGNs[0]):
						files[-1]['id'] = line[len(BGNs[0]):]
					elif line.startswith(BGNs[1]):
						files[-1]['id'] = line[len(BGNs[1]):]
			else:
				if 'id' in files[-1].keys():
					if line.startswith(BGNs[0]) and line.endswith(END) and line[len(BGNs[0]):-len(END)] == files[-1]['id']:
						files[-1]['data'] = bytes(files[-1]['data'][:-2])
						files.append({'data': bytearray()})
						binary = 0
						continue
					elif line.startswith(BGNs[1]) and line.endswith(END) and line[len(BGNs[1]):-len(END)] == files[-1]['id']:
						files[-1]['data'] = bytes(files[-1]['data'][:-2])
						files.append({'data': bytearray()})
						binary = 0
						continue
				files[-1]['data'] += line + b'\r\n'
		return files[:-1]

	def __init__(self, header: str, content: bytes, client_address: tuple[str, int]):
		def get_args(text):
				return {} if text == '' else {pair.split('=')[0]: '='.join(pair.split('=')[1:]) for pair in text.split('&')}
		
		meta = header.split('\n')[0].strip().replace('\r','').split(' ')
		self.header = {'method': meta[0], 'link': ' '.join(meta[1:-1]), 'ver': meta[-1], 'data': {'user-agent': '', 'Accept': '', 'Accept-Encoding': '', 'Accept-Language': ''}}
		header = self.parse_http_header(header)
		self.content = self.parse_http_content(content)
		self.header['data'].update(header)
		self.ip, self.port = client_address[:2]
		self.method = self.header['method']
		self.version = self.header["ver"]
		self.full_link = urllib.parse.unquote(self.header["link"])
		if 'Host' not in self.header['data'].keys():
			print(self.header)
		self.host = self.header["data"]["Host"]
		self.user_agent = self.header["data"]["User-Agent"] if 'User-Agent' in self.header['data'].keys() else self.header['data']['user-agent']
		self.accept = self.header["data"]["Accept"].split(',')
		self.encoding = self.header["data"]["Accept-Encoding"].split(',')
		self.language = self.header["data"]["Accept-Language"].split(',')
		self.link = self.full_link[:(self.full_link.index('?') if '?' in self.full_link else None)]
		self.args = get_args(self.full_link[(self.full_link.index('?')+1 if '?' in self.full_link else len(self.full_link)):])
		self.cookies = {c.split('=')[0]:c.split('=')[1] for c in self.header["data"]["Cookie"].split(';')} if 'Cookie' in self.header['data'] else []

	def __str__(self):
		RESET = '\u001b[0m'
		GRAY = '\u001b[38;2;127;127;127m'

		return f'{GRAY}[{self.method}]{RESET} request {self.full_link} from {"" if "." in self.ip else "["}{self.ip}{"" if "." in self.ip else "]"}:{self.port} on {self.host}'
