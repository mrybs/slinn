from slinn import *


dp = Dispatcher()

@dp(LinkFilter('api'))
def api(request):
    return HttpJSONAPIResponse(status='ok')

@dp(LinkFilter(''))
@dp(LinkFilter('index'))
def index(request):
    return HttpRedirect('/helloworld')

@dp(AnyFilter)
def helloworld(request):
    return HttpResponse('Hello, world!')
