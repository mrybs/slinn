import dexir
import time


GREEN = '\u001b[32m'
BLUE = '\u001b[34m'
RESET = '\u001b[0m'
BOLD = '\u001b[1m'

if __name__ == '__main__':
    _start = time.time()
    data = 'lolkek <% echo( "vaceslav") %><% pull("zero", 10, "xyu", 30, "cm") %><% lol kek 4eburek %> 4eburek'
    l = dexir.Lexer(data)
    lexemes = []
    while lexeme := l.peek():
        lexemes.append(lexeme)
    print(f"""Data {BOLD}{BLUE}"{data}{RESET}"\nhas parsed as:\n{BOLD}{GREEN}{chr(10).join(str(lexeme) for lexeme in lexemes)}{RESET}\nin {BOLD}{(time.time()-_start)*1000}{RESET} milliseconds""")
    for lexeme in lexemes:
        p = lexeme.preprocess()
        if type(p) != str:
            print(f'{BLUE}|{RESET}'.join(str(token) for token in p), end='')
        else:
            print(p, end='')
