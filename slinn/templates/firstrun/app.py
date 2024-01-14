from slinn import Dispatcher, Filter, HttpResponse
import slinn
 
dp_firstrun = Dispatcher('.*')

def read(filename):
    file = open(filename, 'r')
    data = file.read()
    file.close()
    return data

# Write your code down here  
@dp_firstrun.route(Filter('/styles.css'))
def colorscss(request):
    return HttpResponse(read('templates_data/firstrun/styles.css'))
                       
@dp_firstrun.route(Filter('.*'))
def index(request):
    return HttpResponse(read('templates_data/firstrun/slinn.html').replace('{% version %}', slinn.version.split()[1]), content_type='text/html')
