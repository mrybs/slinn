from slinn.filter import Filter


class LinkFilter(Filter):
	def __init__(self, _filter: str, methods: list[str]=None):
		self.filter = r'\/?' + _filter.replace('/', r'\/') + r'(\/.*)?'
		self.methods = ['GET', 'POST'] if methods is None else methods
