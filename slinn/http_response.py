import slinn, gzip


class HttpResponse:
    """
    Base class for all responses
    """
    def __init__(self, payload: any, data: list[tuple] = None, status: str = '200 OK',
                 content_type: str = 'text/plain') -> None:
        self.payload = str(payload).encode() if type(payload) in [str, int, float, bool] else bytes(payload)
        self.data = data if data is not None else [('Content-Type', content_type), ('Server', slinn.version)] \
                                                  + [('Content-Length', len(self.payload))]
        self.status = status
        self.gzip = gzip

    def set_cookie(self, key: str, value: any, attributes: dict = None) -> None:
        if attributes is None:
            attributes = {}
        self.data.append(('Set-Cookie', f'{key}={value}' + attributes),
                         ''.join(
                             [f'; {key}' + '' if type(attributes[key]) is bool else f'={attributes["key"]}' for key in
                              attributes.keys()]))

    def make(self, version: str = 'HTTP/2.0', use_gzip: bool = True) -> bytes:
        return (f'{version} {self.status}' + '\r\n'
                + "\r\n".join([str(dat[0]) + ": " + str(dat[1]) for dat in self.data
                               + ([('Content-Encoding', 'gzip')] if use_gzip else [])]) + '\r\n\r\n').encode() \
            + (gzip.compress(self.payload) if use_gzip else self.payload)
