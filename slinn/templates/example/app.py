from slinn import *

dp = Dispatcher()


@dp(LinkFilter('api'))
def api(request: Request) -> None:
    request.respond(JSONAPIResponse, status='ok')


@dp(LinkFilter(''))
@dp(LinkFilter('index'))
def index(request: Request) -> None:
    request.respond(Redirect, '/helloworld')


@dp(AnyFilter)
def helloworld(request: Request) -> None:
    request.respond(Response, 'Hello, world!')
