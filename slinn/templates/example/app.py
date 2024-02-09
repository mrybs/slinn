from slinn import Server, Dispatcher, AnyFilter, LinkFilter, HttpResponse, HttpAPIResponse, Address


dp = Dispatcher()


@dp(LinkFilter('api'))
def api(request):
    return HttpAPIResponse('{"status": "ok"}')


@dp(AnyFilter)
def helloworld(request):
     return HttpResponse('Hello world!')
