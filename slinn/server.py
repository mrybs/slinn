from slinn import Request, Address, Filter, utils
import socket, ssl, time, os, traceback


class Server:
	class Handle:
		def __init__(self, filter: Filter, function):
			self.filter = filter
			self.function = function
	
	def __init__(self, *dispatchers: tuple, smart_navigation: bool=True, ssl_fullchain: str=None, ssl_key: str=None, delay: float=0.05, timeout: float=0.03, max_bytes_per_recieve: int=4096, max_bytes: int=4294967296):
		self.dispatchers = dispatchers
		self.smart_navigation = smart_navigation
		self.server_socket = None
		self.ssl = ssl_fullchain is not None and ssl_key is not None
		self.ssl_cert, self.ssl_key = ssl_fullchain, ssl_key
		self.ssl_context = None
		self.waiting = False
		self.thread = None
		self.delay = delay
		self.timeout = timeout
		self.max_bytes_per_recieve = max_bytes_per_recieve
		self.max_bytes = max_bytes
		self.__address = None

	def reload(self, *dispatchers: tuple):
		self.waiting = True
		if self.thread is not None:
			self.thread.stop()
			try:
				self.thread.join()
			except RuntimeError:
				pass
		self.dispatchers = dispatchers
		if utils.check_socket(self.server_socket):
			self.server_socket.close()
		if self.__address is not None:
			self.listen(self.__address)

	def address(self):
		return f'HTTP{"S" if self.ssl else ""} server is available on http{"s" if self.ssl else ""}://{"" if "." in self.host else "["}{self.host}{"" if "." in self.host else "]"}{(":"+str(self.port) if self.port != 443 else "") if self.ssl else (":"+str(self.port )if self.port != 80 else "")}/'
		
	def listen(self, address: Address):		
		self.__address = address
		self.host, self.port = address.host, address.port
		if socket.has_dualstack_ipv6() and '.' not in self.host and ':' not in self.host:
			self.server_socket = socket.create_server((self.host, self.port), family=socket.AF_INET6, dualstack_ipv6=True)
		elif ':' in self.host:
			self.server_socket = socket.create_server((self.host, self.port), family=socket.AF_INET6)
		else:
			self.server_socket = socket.create_server((self.host, self.port), family=(socket.AF_INET if '.' in self.host else socket.AF_INET6))
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		if self.ssl:
			self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
			self.ssl_context.load_cert_chain(certfile=self.ssl_cert, keyfile=self.ssl_key)
		self.server_socket.listen()
		print(self.address())
		self.waiting = False
		try:
			while utils.check_socket(self.server_socket):
				if not self.waiting:
					self.thread = utils.StoppableThread(target=self.handle_request)
					self.thread.start()
				time.sleep(self.delay)
		except KeyboardInterrupt:
			print('Got KeyboardInterrupt, halting the application...')
			if utils.check_socket(self.server_socket):
				self.server_socket.close()
			os._exit(0)
						
	def handle_request(self):
		try:
			self.waiting = True
			client_socket, client_address = self.server_socket.accept()
			if self.ssl:
				client_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)
			self.waiting = False
			try:
				client_socket.settimeout(self.timeout)
				data = bytearray()
				while len(data) < self.max_bytes:
					try:
						b = client_socket.recv(self.max_bytes_per_recieve)
						data += b
					except TimeoutError:
						break
					
				data = data.split(b'\r\n\r\n')
				header = data[0].decode()
				content = b'\r\n\r\n'.join(data[1:])
				
				if header == '':
					return

				request = Request(header, content, client_address)
				print(request)
			except KeyError:
				if utils.check_socket(client_socket):
					client_socket.close()
				return print('Got KeyError, probably invalid request. Ignore')
			except UnicodeDecodeError:
				if utils.check_socket(client_socket):
					client_socket.close()
				return print('Got UnocodeDecodeError, probably invalid request. Ignore')
			except ConnectionResetError:
				return print('Connection reset by client')
			except OSError:
				return print('Connection closed')
			for dispatcher in self.dispatchers:
				if True in [utils.restartswith(request.host, host) for host in dispatcher.hosts]:
					if self.smart_navigation:
						sizes = [handle.filter.size(request.link, request.method) for handle in dispatcher.handles]
						if sizes != []:
							handle = dispatcher.handles[sizes.index(max(sizes))]
							if handle.filter.check(request.link, request.method):
								if utils.check_socket(client_socket):
									client_socket.sendall(handle.function(request).make(request.version))
									client_socket.close()
								return
					else:
						for handle in dispatcher.handles:
							if handle.filter.check(request.link, request.method):
								if utils.check_socket(client_socket):
									client_socket.sendall(handle.function(request).make(request.version))
									client_socket.close()
								return
		except ssl.SSLError:
			print('During handling request, an exception has occured:')
			traceback.print_exc()
			print('Got ssl.SSLError, reloading...')
			self.reload(*self.dispatchers)
		except Exception:
			print('During handling request, an exception has occured:')
			traceback.print_exc()
			self.waiting = False
