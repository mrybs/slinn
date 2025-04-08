import enum
import tokenizer


class Lexer:
    def __init__(self, data: str):
        self.data = data
        self.cursor = 0

    def _peek(self):
        i = self.cursor
        for i in range(self.cursor, len(self.data) + 1):
            if self.data[i + 1:i + 3] == '<%':
                return self.cursor, i + 1
            if self.data[i + 1:i + 3] == '%>':
                return self.cursor, i + 3
        return None if i == self.cursor else (self.cursor, i)

    def peek(self):
        peeked = self._peek()
        if type(peeked) == tuple:
            self.cursor = peeked[1]
            return Token(self.data[peeked[0]:peeked[1]]).to_lexeme()


class LexemesKind(enum.Enum):
    PLAIN = 0
    CODE = 1


class Lexeme:
    def __init__(self, kind: LexemesKind, data: str):
        self.kind = kind
        self.data = data

    def __repr__(self):
        return f'{self.kind.name} Lexeme "{self.data}"'

    def preprocess(self):
        if self.kind == LexemesKind.PLAIN:
            return self.data
        if self.kind == LexemesKind.CODE:
            t = tokenizer.Tokenizer(self.data)
            tokens = []
            while token := t.peek():
                tokens.append(token)
            return tokens


class Token:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return self.data

    def to_lexeme(self):
        if self.data.startswith('<%') and self.data.endswith('%>'):
            return Lexeme(LexemesKind.CODE, self.data[2:-2].strip())
        return Lexeme(LexemesKind.PLAIN, self.data)
