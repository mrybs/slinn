from slinn import Dispatcher, AnyFilter, LinkFilter, HttpResponse, HttpAPIResponse


dp = Dispatcher()


@dp(LinkFilter('api'))
def api(request):
    return HttpAPIResponse('{"status": "ok"}')


@dp(AnyFilter)
def helloworld(request):
     return HttpResponse('Hello, World!')
