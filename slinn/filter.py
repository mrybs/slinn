from slinn import utils


class Filter:
	def __init__(self, filter: str, methods: list[str]=None):
		self.filter = filter
		self.methods = ['GET', 'POST'] if methods is None else methods
		
	def check(self, text: str, method: str) -> bool:
		return utils.restartswith(text, self.filter) and method.upper() in self.methods