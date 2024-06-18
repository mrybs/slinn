from slinn import *


def read(filename) -> str:
    _file = open(filename, 'r', encoding='utf-8')
    data = _file.read()
    _file.close()
    return data


dp = Dispatcher()


@dp(LinkFilter('styles.css'))
def styles(request: Request) -> None:
    request.respond(Render, 'templates_data/firstrun/styles.css')


@dp(AnyFilter)
def index(request: Request) -> None:
    request.respond(Response, read('templates_data/firstrun/slinn.html').replace('{% version %}', version.split()[2]), content_type='text/html')
