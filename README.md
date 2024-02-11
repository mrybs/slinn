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
Server(*dispatchers: list[Dispatcher], ssl_cert: str=None, ssl_key: str=None, http_ver: str='2.0')
server.address() -> str
server.reload(*dispatchers: list[Dispatcher])
server.listen(address: Address)
```

```python
Address(port: int, host: str=None)
```

```python
Dispatcher(hosts: list=None)
dispatcher.route(filter: Filter)
```

```python
Filter(filter: str, methods: list[str]=None)
_filter.check(text: str, method: str) -> bool
_filter.size(text: str, method: str) -> int  # Special method for Smart Navigation

# LinkFilter inherits from Filter
LinkFilter(filter: str, methods: list[str]=None)
link_filter.check(text: str, method: str) -> bool

# AnyFilter as same as Filter('.*')
```

```python
HttpResponse(payload, data: list[tuple]=None, status: str='200 OK', content_type: str='text/plain')
HttpResponse.set_cookie(key: str, value)
HttpResponse.make(type: str='HTTP/2.0') -> str

HttpAPIResponse(payload, data: list[tuple]=None, status: str='200 OK', content_type: str='text/plain')
httpAPIResponse.set_cookie(key: str, value)
httpAPIResponse.make(type: str='HTTP/2.0') -> str

# HttpRedirect inherits from HttpResponse
HttpRedirect(location: str)
```

```python
Request(http_data: str, client_address: tuple[str, int])
```
