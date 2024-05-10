from slinn.http_response import HttpResponse


class HttpRender(HttpResponse):
    
    """
    Renders any file to HttpResponse-based object
    """

    def __init__(self, file_path: str, data: list[tuple] = None, status: str = '200 OK') -> None:
        self.file_path = file_path
        self.file_extension = file_path.split('.')[-1]
        self.data = data
        self.status = status

    def make(self, version: str = 'HTTP/2.0', use_gzip: bool = True) -> bytes:
        content_type = 'text/plain'
        match self.file_extension:
            case 'html':
                with open(self.file_path, 'r') as f:
                    self.payload = f.read()
                    content_type = 'text/html'
            case 'css':
                with open(self.file_path, 'r') as f:
                    self.payload = f.read()
                    content_type = 'text/css'
            case 'js':
                with open(self.file_path, 'r') as f:
                    self.payload = f.read()
                    content_type = 'text/javascript'
            case 'png':
                with open(self.file_path, 'rb') as f:
                    self.payload = f.read()
                    content_type = 'image/png'
            case 'jpg':
                with open(self.file_path, 'rb') as f:
                    self.payload = f.read()
                    content_type = 'image/jpg'
            case 'svg':
                with open(self.file_path, 'rb') as f:
                    self.payload = f.read()
                    content_type = 'image/svg'
        self.data = self.data if self.data is not None else [('Content-Type', content_type),
                                                             ('Server', 'Slinn'), ('Content-Length', len(self.payload))]
        return super().make(version, use_gzip)
