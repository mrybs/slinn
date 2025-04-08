class Token:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return self.data


STR_CHARS = '"\'`'
SINGLE_CHARS = '()[]{},.=+-*/ \n'

class Tokenizer:
    def __init__(self, data):
        self.data = data
        self.cursor = 0

    def _peek(self):
        str_char = None
        i = self.cursor
        for i in range(self.cursor, len(self.data)):
            current_char = self.data[i]
            next_char = self.data[i + 1] if i + 1 < len(self.data) else ''
            if not str_char and self.cursor == i and current_char in STR_CHARS:
                str_char = current_char
            elif ((not str_char and next_char in STR_CHARS) or
                  (str_char == current_char) or
                  (next_char in SINGLE_CHARS) or
                  (current_char in SINGLE_CHARS)
            ):
                return self.cursor, i + 1
        return None if self.cursor == i else (self.cursor, i)

    def peek(self):
        peeked = self._peek()
        if type(peeked) == tuple:
            self.cursor = peeked[1]
            token = Token(self.data[peeked[0]:peeked[1]].strip())
            if token.data == '':
                return self.peek()
            return token
