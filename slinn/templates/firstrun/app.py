from slinn import Dispatcher, LinkFilter, AnyFilter, HttpResponse
import slinn

def read(filename):
    file = open(filename, 'r', encoding='utf-8')
    data = file.read()
    file.close()
    return data

dp = Dispatcher()

@dp(LinkFilter('styles.css'))
def styles(request):
    return HttpResponse(read('templates_data/firstrun/styles.css'))

@dp(AnyFilter)
def index(request):
    return HttpResponse(read('templates_data/firstrun/slinn.html').replace('{% version %}', slinn.version.split()[2]), content_type='text/html')
