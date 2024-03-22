class File:
    def __init__(self, id: str=None, data: bytes|bytearray=bytearray()):
        self.id = id
        self.data = data
        self.header = {}
