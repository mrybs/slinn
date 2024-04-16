class File:
    def __init__(self, file_id: str = None, data: bytes | bytearray = bytearray()) -> None:
        self.id = file_id
        self.data = data
        self.header = {}
