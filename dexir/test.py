import lexer
import time


GREEN = '\u001b[32m'
BLUE = '\u001b[34m'
RESET = '\u001b[0m'
BOLD = '\u001b[1m'

if __name__ == '__main__':
    _start = time.time()
    data = 'lolkek <% echo `vaceslav` %><% echo `daun` %> 4eburek'
    l = lexer.Lexer(data)
    lexemes = []
    while lexeme := l.peek():
        lexemes.append(lexeme)
    print(f"""Data {BOLD}{BLUE}"{data}{RESET}"\nhas parsed as:\n{BOLD}{GREEN}{chr(10).join(str(lexeme) for lexeme in lexemes)}{RESET}\nin {BOLD}{(time.time()-_start)*1000}{RESET} milliseconds""")