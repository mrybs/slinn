from slinn import HttpResponse


class HttpRedirect(HttpResponse):
	def __init__(self, location: str):
		super().__init__('', [('Location',location)], status='307 Temporary Redirect')