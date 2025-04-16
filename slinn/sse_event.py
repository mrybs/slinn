from slinn import HttpResponseChunk


class SSEEvent(HttpResponseChunk):
    def __init__(self, data):
        super().__init__(payload=f'data: {data}\n\n')
