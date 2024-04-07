from slinn import Server, Filter


class Dispatcher:
	def __init__(self, *hosts: tuple):
		self.handles = []
		self.hosts = hosts if list(hosts) != [] else ['.*']
		
	def __call__(self, filter: Filter):
		def decorator(func):
			self.handles.append(Server.Handle(filter, func))
		return decorator	