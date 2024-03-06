# Slinn is a HTTPS and HTTP server framework

### Create project
##### Unix-like (Linux, MacOS, FreeBSD...):
```bash
python3 -m slinn create helloworld
cd helloworld
venv/bin/python manage.py create localhost host=localhost host=127.0.0.1
venv/bin/python manage.py run 
```

##### Windows:
```bat
py -m slinn create helloworld
cd helloworld
venv\Scripts\activate
py manage.py create localhost host=localhost host=127.0.0.1
py manage.py run 
```

#### Simple example
```python
# localhost/app.py

from slinn import Dispatcher, AnyFilter, LinkFilter, HttpResponse, HttpAPIResponse


dp = Dispatcher('localhost', '127.0.0.1')


@dp(LinkFilter('api'))
def api(request):
    return HttpAPIResponse('{"status": "ok"}')


@dp(AnyFilter)
def helloworld(request):
     return HttpResponse('Hello world!')

```

To config project you should edit `./project.json`

To config app you should edit `./%app%/config.json`

#### Functions:
```python
from slinn import Server

server = Server(*dispatchers: list[Dispatcher], ssl_cert: str=None, ssl_key: str=None, http_ver: str='2.0')
server.address() -> str
server.reload(*dispatchers: list[Dispatcher])
server.listen(address: Address)
```

```python
from slinn import Address

address = Address(port: int, host: str=None)
```

```python
from slinn import Dispatcher

dispatcher = Dispatcher(hosts: list=None)
dispatcher.route(filter: Filter)
```

```python
from slinn import Filter

_filter = Filter(filter: str, methods: list[str]=None)
_filter.check(text: str, method: str) -> bool
_filter.size(text: str, method: str) -> int  # Special method for Smart Navigation

# LinkFilter inherits from Filter
from slinn import LinkFilter

link_filter = LinkFilter(filter: str, methods: list[str]=None)
link_filter.check(text: str, method: str) -> bool

# AnyFilter as same as Filter('.*')
from slinn import AnyFilter
```

```python
from slinn import HttpResponse

http_response = HttpResponse(payload, data: list[tuple]=None, status: str='200 OK', content_type: str='text/plain')
http_response.set_cookie(key: str, value)
http_response.make(type: str='HTTP/2.0') -> str

# HttpAPIResponse inherits from HttpResponse
from slinn import HttpAPIResponse

http_api_response = HttpAPIResponse(payload, data: list[tuple]=None, status: str='200 OK', content_type: str='text/plain')
http_api_response.set_cookie(key: str, value)
http_api_response.make(type: str='HTTP/2.0') -> str

# HttpRedirect inherits from HttpResponse
from slinn import HttpRedirect

HttpRedirect(location: str)
```

```python
from slinn import Request

request = Request(http_data: str, client_address: tuple[str, int])

# Attributes
request.ip, request.port  # Client`s IP and port
request.method  # HTTP method
request.version  # HTTP version
request.full_link  # Full link(path and params)
request.host  # Requested host
request.user_agent  # Client`s user agent
request.accept  # maybe supported technologies
request.encoding  # Supported encodings
request.language  # Client`s language
request.link  # Link(only path)
request.args  # GET args
request.cookies  # All saved cookies
```
