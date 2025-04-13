"""Import slinn`s modules"""
from slinn import Dispatcher, LinkFilter, Server


class ApiDispatcher(Dispatcher):
    """FastAPI-style dispatcher for CRUD methods"""
    def __init__(self, *hosts, prefix: str=''):
        super().__init__(*hosts)
        self.prefix = prefix

    def get(self, path: str = '/'):
        """HTTP-GET Requests handler creator"""
        def decorator(func):
            self.handles.append(Server.Handle(LinkFilter(self.prefix+path, ('GET',)), func))
            return func
        return decorator

    def post(self, path: str = '/'):
        """HTTP-POST Requests handler creator"""
        def decorator(func):
            self.handles.append(Server.Handle(LinkFilter(self.prefix+path, ('POST',)), func))
            return func
        return decorator

    def patch(self, path: str = '/'):
        """HTTP-PATCH Requests handler creator"""
        def decorator(func):
            self.handles.append(Server.Handle(LinkFilter(self.prefix+path, ('PATCH',)), func))
            return func
        return decorator

    def put(self, path: str = '/'):
        """HTTP-PUT Requests handler creator"""
        def decorator(func):
            self.handles.append(Server.Handle(LinkFilter(self.prefix+path, ('PUT',)), func))
            return func
        return decorator

    def delete(self, path: str = '/'):
        """HTTP-DELETE Requests handler creator"""
        def decorator(func):
            self.handles.append(Server.Handle(LinkFilter(self.prefix+path, ('DELETE',)), func))
            return func
        return decorator
