from slinn import HttpResponse


class EmptyHttpResponse(HttpResponse):
    def __init__(self) -> None:
        super().__init__('', status='204 No Content')
