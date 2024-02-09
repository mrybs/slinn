from slinn import utils


class LinkFilter:
	def __init__(self, _filter: str, methods: list[str]=None):
		self.filter = '\\/?' + _filter.replace('/', '\\/') + '(\\/.*)?'
		self.methods = ['GET', 'POST'] if methods is None else methods
		
	def check(self, text: str, method: str) -> bool:
		return utils.restartswith(text, self.filter) and method.upper() in self.methods