import socket


class Address:
	def __init__(self, port: int, host: str=None):
		self.port = port
		self.domain = host
		if host not in [None, '']:
			family, socktype, proto, cannonname, sockaddr = socket.getaddrinfo(host, self.port, socket.AF_UNSPEC, socket.SOCK_DGRAM, 0, socket.AI_PASSIVE)[0]
			self.host = sockaddr[0]
		else:
			self.host = ''