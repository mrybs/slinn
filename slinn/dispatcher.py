from slinn import Server, Filter


class Dispatcher:
	def __init__(self, *hosts: list):
		self.handles = []
		self.hosts = hosts if list(hosts) != [] else ['.*']
		
	def route(self, filter: Filter):
		def decorator(func):
			self.handles.append(Server.Handle(filter, func))
		return decorator	