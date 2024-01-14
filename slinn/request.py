class Request:	
	def __init__(self, http_data: str, client_address: tuple[str, int]):
		def parse_http(http):
			result = {'data': {}}
			for line in http.split('\n'):
				if len(line.split(':')) > 1:
					key, value = line.split(':')[0], ':'.join(line.split(':')[1:])
					result['data'][key.strip()]=value.strip().replace('\r','')
				elif len(line.split(' ')) == 3:
					params = line.strip().replace('\r','').split(' ')
					result = {'method': params[0], 'link': params[1], 'ver': params[2]} | result
			return result
			
		def get_args(text):
				return {} if text == '' else {pair.split('=')[0]: pair.split('=')[1] for pair in text.split('&')}
		
		self.data = {'data': {'user-agent': '', 'Accept': '', 'Accept-Encoding': '', 'Accept-Language': ''}}
		data = parse_http(http_data)
		self.data['data'].update(data['data'])
		del data['data']
		self.data.update(data)
		self.ip, self.port = client_address[:2]
		self.method = self.data['method']
		self.version = self.data["ver"]
		self.full_link = self.data["link"]
		self.host = self.data["data"]["Host"]
		self.user_agent = self.data["data"]["User-Agent"] if 'User-Agent' in self.data['data'].keys() else self.data['data']['user-agent']
		self.accept = self.data["data"]["Accept"].split(',')
		self.encoding = self.data["data"]["Accept-Encoding"].split(',')
		self.language = self.data["data"]["Accept-Language"].split(',')
		self.link = self.full_link[:(self.full_link.index('?') if '?' in self.full_link else None)]
		self.args = get_args(self.full_link[(self.full_link.index('?')+1 if '?' in self.full_link else len(self.full_link)):])
		self.cookies = {c.split('=')[0]:c.split('=')[1] for c in self.data["data"]["Cookie"].split(';')} if 'Cookie' in self.data['data'] else []