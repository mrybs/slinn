import slinn


class HttpResponseChunk:
    def __init__(self, payload: any) -> None:
        self.payload = slinn.utils.representate(payload)

    def make(self, version: str = 'HTTP/1.0', use_gzip: bool = False) -> bytes:
        return self.payload
