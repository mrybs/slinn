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

Excepted output
```
$ venv/bin/python manage.py run
Loading config...
Apps: firstrun
Debug mode enabled
Smart navigation enabled

Starting server...
HTTP server is available on http://[::1]:8080/
```

To config project you should edit `./project.json`

To config app you should edit `./%app%/config.json`

### Create classic project
##### Unix-like (Linux, MacOS, FreeBSD...):
```bash 
mkdir helloworld 
cd helloworld
python3 -m venv venv
venv/bin/activate
```

##### Windows:
```bat
mkdir helloworld 
cd helloworld
python3 -m venv venv
venv\Scripts\activate
```

You should add this code to example `example.py`
```
Server(dp).listen(Address(8080))
```
then write `python example.py`

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

# To add handler into dispatcher
@dispatcher(filter: Filter)
def handler(request: Request):
    ...

# handler should return HttpResponse-based object
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
from slinn import HttpResponse, HttpRedirect, HttpAPIResponse, HttpJSONResponse, HttpJSONAPIResponse

http_response = HttpResponse(payload, data: list[tuple]=None, status: str='200 OK', content_type: str='text/plain')
http_response.set_cookie(key: str, value)
http_response.make(type: str='HTTP/2.0') -> str

HttpResponse('<h1>Hello world</h1>', content_type='text/html')

# HttpAPIResponse inherits from HttpResponse
# HttpAPIResponse sets Access-Control-Allow-Origin to '*'

HttpAPIResponse('{"status": "ok", "username": "mrybs"}')

# HttpRedirect inherits from HttpResponse
HttpRedirect(location: str)

HttpRedirect('slinn.miotp.ru')

# HttpJSONResponse for responding JSON 
HttpJSONResponse(**payload)

HttpJSONResponse(status='this action is forbidden', _status='403 Forbidden')

# HttpJSONAPIResponse is like HttpJSONResponse, but it sets Access-Control-Allow-Origin to '*'

HttpJSONAPIResponse(code=43657, until=1719931149)
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
