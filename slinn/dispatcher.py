from __future__ import annotations
from slinn import Handle, Filter, LinkFilter


class Dispatcher:

    """
    Class for handling requests
    """
    
    def __init__(self, *hosts: tuple) -> None:
        self.handles = []
        self.hosts = hosts if hosts != () else ('.*', )

    def __call__(self, regexp: Filter) -> callable:
        def wrapper(func):
            self.handles.append(Handle(regexp, func))
            return func

        return wrapper

    def static(self, link: str, http_response, *args, **kwargs) -> Dispatcher:
        self.handles.append(Handle(LinkFilter(link), lambda: http_response(*args, **kwargs)))
        return self
