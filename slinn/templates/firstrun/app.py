from slinn import Dispatcher, Filter, HttpResponse
import slinn
 
dp = Dispatcher()

def read(filename):
    file = open(filename, 'r', encoding='utf-8')
    data = file.read()
    file.close()
    return data

# Write your code down here  
@dp(Filter('/styles.css'))
def colorscss(request):
    return HttpResponse(read('templates_data/firstrun/styles.css'))
                       
@dp(Filter('.*'))
def index(request):
    return HttpResponse(read('templates_data/firstrun/slinn.html').replace('{% version %}', slinn.version.split()[1]), content_type='text/html')
