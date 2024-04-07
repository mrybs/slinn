from slinn import Request, Address, Filter, utils
import socket, ssl, time, os, traceback


class Server:
	class Handle:
		def __init__(self, filter: Filter, function):
			self.filter = filter
			self.function = function
	
	def __init__(self, *dispatchers: tuple, smart_navigation: bool=True, ssl_fullchain: str=None, ssl_key: str=None, timeout: float=0.03, max_bytes_per_recieve: int=4096, max_bytes: int=4294967296):
		self.dispatchers = dispatchers
		self.smart_navigation = smart_navigation
		self.server_socket = None
		self.ssl = ssl_fullchain is not None and ssl_key is not None
		self.ssl_cert, self.ssl_key = ssl_fullchain, ssl_key
		self.ssl_context = None
		self.thread = None
		self.timeout = timeout
		self.max_bytes_per_recieve = max_bytes_per_recieve
		self.max_bytes = max_bytes
		self.__address = None

	def reload(self, *dispatchers: tuple):
		if self.thread is not None:
			self.thread.stop()
			try:
				self.thread.join()
			except RuntimeError:
				pass
		self.dispatchers = dispatchers
			

	def address(self, port: int, domain: str):
		return f'HTTP{"S" if self.ssl else ""} server is available on http{"s" if self.ssl else ""}://{"[" if ":" in host else ""}{host}{"]" if ":" in host else ""}{(":"+str(port) if port != 443 else "") if self.ssl else (":"+str(port )if port != 80 else "")}/'
		
	def listen(self, address: Address):		
		self.server_socket = None
		if socket.has_dualstack_ipv6() and '.' not in address.host and ':' not in address.host:
			self.server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, dualstack_ipv6=True)
		elif ':' in address.host:
			self.server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		else:
			self.server_socket = socket.socket(socket.AF_INET if '.' in self.host else socket.AF_INET6, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind((address.host, address.port))
		if self.ssl:
			self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
			self.ssl_context.load_cert_chain(certfile=self.ssl_cert, keyfile=self.ssl_key)
		self.server_socket.listen()
		print(self.address(address.port, address.domain))
		try:
			while True:
				utils.StoppableThread(target=self.handle_request, args=self.server_socket.accept()).start()
		except KeyboardInterrupt:
			print('Got KeyboardInterrupt, halting the application...')
			if utils.check_socket(self.server_socket):
				self.server_socket.close()
			os._exit(0)
						
	def handle_request(self, client_socket, client_address):
		try:
			if self.ssl:
				client_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)
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
				return print('Got KeyError, probably invalid request. Ignore')
			except UnicodeDecodeError:
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
