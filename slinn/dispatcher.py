from __future__ import annotations
from slinn import Server, Filter, LinkFilter


class Dispatcher:
    def __init__(self, *hosts: tuple) -> None:
        self.handles = []
        self.hosts = hosts if list(hosts) != [] else ['.*']

    def __call__(self, regexp: Filter) -> callable:
        def decorator(func):
            self.handles.append(Server.Handle(regexp, func))
            return func

        return decorator

    def static(self, link: str, http_response, *args, **kwargs) -> Dispatcher:
        self.handles.append(Server.Handle(LinkFilter(link), lambda: http_response(*args, **kwargs)))
        return self
