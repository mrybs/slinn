import gzip
import slinn


class HttpResponse():
    """
    Base class for all responses
    """

    def __init__(self, payload: any, data: list[tuple] = None, status: str = '200 OK',
                 content_type: str = 'text/plain; charset=utf-8') -> None:
        self.payload = slinn.utils.representate(payload)
        self.data = [('Content-Type', content_type), ('Server', slinn.version)] + [('Content-Length', len(self.payload))] +\
            (data if data is not None else [])
        self.status = status

    def set_cookie(self, key: str, value: any, attributes: dict = None) -> None:
        if attributes is None:
            attributes = {}
        self.data.append(('Set-Cookie', f'{key}={value}' +
                         ''.join(
                             [f'; {key}' + ('' if type(attributes[key]) is bool else f'={attributes[key]}') for key in
                              attributes.keys()])))

    def make(self, version: str = 'HTTP/1.0', use_gzip: bool = False) -> bytes:
        return (f'{version} {self.status}' + '\r\n'
                + "\r\n".join([str(dat[0]) + ": " + str(dat[1]) for dat in self.data
                               + ([('Content-Encoding', 'gzip')] if use_gzip else [])]) + '\r\n\r\n').encode('utf-8') \
            + (gzip.compress(self.payload) if use_gzip else self.payload)
