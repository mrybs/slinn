from slinn import utils


class Filter:
	def __init__(self, filter: str, methods: tuple=None):
		self.filter = filter
		self.methods = ('GET', 'POST') if methods is None else methods
		
	def check(self, text: str, method: str) -> bool:
		return utils.rematcheswith(text, self.filter) and method.upper() in self.methods
	
	def size(self, text: str, method: str) -> int:
		a = utils.min_restartswith_size(text, self.filter) if self.check(text, method) else 2147483647
		b = utils.Bmin_restartswith_size(text, self.filter) if self.check(text, method) else 2147483647
		if not self.check(text, method):
			return -1
		elif a == 2147483647:
			return 0
		else:
			return b