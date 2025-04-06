class Token:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return self.data

class Lexeme:
    def __init__(self, type, data: str):
        self.type = type
        self.data = data

    def __repr__(self):
        return f'Lexeme(type={self.type}; data="{self.data}")'


def token_to_lexeme(token: Token):
    if token.data.startswith('<%') and token.data.endswith('%>'):
        return Lexeme('code', token.data[2:-2].strip())
    return Lexeme('plain', token.data)


class Lexer:
    def __init__(self, data: str):
        self.data = data
        self.cursor = 0

    def peek(self):
        i = self.cursor
        while i < len(self.data):
            if self.data[i+1:i+3] == '<%':
                token = token_to_lexeme(Token(self.data[self.cursor:i+1]))
                self.cursor = i+1
                return token
            if self.data[i+1:i+3] == '%>':
                token = token_to_lexeme(Token(self.data[self.cursor:i+3]))
                self.cursor = i+3
                return token
            i += 1
        if i == self.cursor:
            return None
        token = token_to_lexeme(Token(self.data[self.cursor:i]))
        self.cursor = i
        return token

