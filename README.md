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
Delay: 50.0ms

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

server = Server(*dispatchers: tuple, ssl_cert: str=None, ssl_key: str=None, delay: float=0.05, timeout: float=0.03, max_bytes_per_recieve: int=4096, max_bytes: int=4294967296)  # Main class to run server
server.address() -> str  # Returns info str
server.reload(*dispatchers: tuple)  # Reloads server
server.listen(address: Address)  # Start listening address

Server(dp_api, dp_gui, ssl_cert='fullchain.pem', ssl_key='privkey.pem')
```

```python
from slinn import Address

address = Address(port: int, host: str=None)  # A structure containing a port and a host; converts dns-address to ip-address

Address(443, 'google.com')
```

```python
from slinn import Dispatcher

dispatcher = Dispatcher(hosts: tuple=None)  # A class that contain many handlers

Dispatcher('localhost', '127.0.0.1', '::1')

# To add handler into dispatcher
@dispatcher(filter: Filter)
def handler(request: Request):
    ...

# handler should return HttpResponse-based object
```

```python
from slinn import Filter, LinkFilter, AnyFilter

_filter = Filter(filter: str, methods: tuple=None)  # This class is used to choose match handler by link; uses regexp
_filter.check(text: str, method: str) -> bool  # Checks for a match by filter
_filter.size(text: str, method: str) -> int  # Special method for Smart Navigation

Filter('/user/.+/profile.*')

# LinkFilter inherits from Filter
LinkFilter('user/.+/profile')

# AnyFilter as same as Filter('.*')
```

```python
from slinn import HttpResponse, HttpRedirect, HttpAPIResponse, HttpJSONResponse, HttpJSONAPIResponse

http_response = HttpResponse(payload: any, data: list[tuple]=None, status: str='200 OK', content_type: str='text/plain')  # This class is used to convert some data to HTTP code
http_response.set_cookie(key: str, value: any)
http_response.make(type: str='HTTP/2.0') -> str

HttpResponse('<h1>Hello world</h1>', content_type='text/html')

# HttpAPIResponse inherits from HttpResponse
# HttpAPIResponse sets Access-Control-Allow-Origin to '*'

HttpAPIResponse('{"status": "ok", "username": "mrybs"}')

# HttpRedirect inherits from HttpResponse
HttpRedirect(location: str)

HttpRedirect('slinn.miotp.ru')

# HttpJSONResponse for responding JSON 
HttpJSONResponse(**payload: dict)

HttpJSONResponse(status='this action is forbidden', _status='403 Forbidden')

# HttpJSONAPIResponse is like HttpJSONResponse, but it sets Access-Control-Allow-Origin to '*'

HttpJSONAPIResponse(code=43657, until=1719931149)
```

```python
from slinn import Request

request = Request(header: str, body: bytes, client_address: tuple[str, int])  # This structure is used in the dispatcher`s handler
request.parse_http_header(http_header: str)  # Parse HTTP request`s header
request.parse_http_body(http_body: body)  # Parse HTTP request`s body if exists
str(request)  # Convert slinn.Request to info text

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
request.files # Uploaded files
```

```python
from slinn import File

file = File(id: str=None, data: bytes|bytearray=bytearray())

# Attributes
file.id  # File`s id 
file.data  # Binary data
file.headers  # Headers such as Content-Disposition
```
