from slinn import Request, Address, utils
import socket, ssl, threading, time, traceback, json, os


class Server:
	class Handle:
		def __init__(self, filter, function):
			self.filter = filter
			self.function = function

	RESET = '\u001b[0m'
	GRAY = '\u001b[38;2;127;127;127m'
	
	def __init__(self, *dispatchers, ssl_fullchain: str=None, ssl_key: str=None, http_ver: str='2.0'):
		self.dispatchers = dispatchers
		self.server_socket = None
		self.ssl = ssl_fullchain is not None and ssl_key is not None
		self.ssl_cert, self.ssl_key = ssl_fullchain, ssl_key
		self.ssl_context = None
		self.http_ver = http_ver
		self.waiting = False
		
	def listen(self, address: Address):		
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
		print(f'HTTP{"S" if self.ssl else ""} server is available on http{"s" if self.ssl else ""}://{"" if "." in self.host else "["}{self.host}{"" if "." in self.host else "]"}{(":"+str(self.port) if self.port != 443 else "") if self.ssl else (":"+str(self.port )if self.port != 80 else "")}/')
		try:
			while True:
				if not self.waiting:
					threading.Thread(target=self.handle_request).start()
				time.sleep(0.1)
		except KeyboardInterrupt:
			print('Got KeyboardInterrupt, halting the application...')
			os._exit(0)
						
	def handle_request(self):
		try:
			self.waiting = True
			client_socket, client_address = self.server_socket.accept()
			if self.ssl:
				client_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)
			self.waiting = False
			try:
				request = Request(client_socket.recv(8192).decode(), client_address)
				print(f'{GRAY}[{request.method}]{RESET} request {request.full_link} from {"" if "." in request.ip else "["}{request.ip}{"" if "." in request.ip else "]"}:{request.port} on {request.host}')
			except UnicodeDecodeError:
				return
			for dispatcher in self.dispatchers:
				if True in [utils.restartswith(request.host, host) for host in dispatcher.hosts]:
					for handle in dispatcher.handles:
						if handle.filter.check(request.link, request.method):
							client_socket.sendall(handle.function(request).make(request.version))
							client_socket.close()
							return
		except Exception:
			print('During handling request, an exception has occured:')
			traceback.print_exc()
			self.waiting = False