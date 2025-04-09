import enum
import tokenizer


class LexemeKind(enum.Enum):
    OBJECT = 0
    OPEN_QUOTE = 1
    CLOSE_QUOTE = 2


class Lexeme:
    def __init__(self, kind: LexemeKind, data: str):
        self.kind = kind
        self.data = data

    def __repr__(self):
        return f'{self.kind.name} Lexeme "{self.data}"'

    @staticmethod
    def determine_kind(token: tokenizer.Token) -> LexemeKind:
        if token.data == '(':
            return LexemeKind.OPEN_QUOTE
        if token.data == ')':
            return LexemeKind.CLOSE_QUOTE
        return LexemeKind.OBJECT


class Lexer:
    def __init__(self, tokens: list[tokenizer.Token]):
        self.tokens = tokens
        self.cursor = 0

    def peek(self):
        if self.cursor >= len(self.tokens):
            return None
        token = self.tokens[self.cursor]
        self.cursor += 1
        return Lexeme(Lexeme.determine_kind(token), token.data)
