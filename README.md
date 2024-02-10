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
venv/Scripts/activate
py manage.py create localhost host=localhost host=127.0.0.1
py manage.py run 
```

#### Simple example
```python
from slinn import Server, Dispatcher, AnyFilter, LinkFilter, HttpResponse, HttpAPIResponse, Address


dp = Dispatcher()


@dp(LinkFilter('api'))
def api(request):
    return HttpAPIResponse('{"status": "ok"}')


@dp(AnyFilter)
def helloworld(request):
     return HttpResponse('Hello world!')

```

To config project you should edit `./project.json`
To config app you should edit `./appname/config.json`

#### Functions:
```python
Server(*dispatchers, ssl_cert: str=None, ssl_key: str=None, http_ver: str='2.0')
server.address() -> str
server.reload(*dispatchers)
server.listen(address: Address)
```

```python
Address(self, port: int, host: str=None)
```

```python
Dispatcher(self, hosts: list=None)
dispatcher.route(self, filter: Filter)
```

```python
Filter(self, filter: str, methods: list[str]=None)
_filter.check(self, text: str, method: str) -> bool

# LinkFilter inherits from Filter
LinkFilter(self, filter: str, methods: list[str]=None)
link_filter.check(self, text: str, method: str) -> bool

# AnyFilter as same as Filter('.*')
```

```python
HttpResponse(self, payload, data: list[tuple]=None, status: str='200 OK', content_type: str='text/plain')
HttpResponse.set_cookie(self, key: str, value)
HttpResponse.make(self, type: str='HTTP/2.0') -> str

HttpAPIResponse(self, payload, data: list[tuple]=None, status: str='200 OK', content_type: str='text/plain')
httpAPIResponse.set_cookie(self, key: str, value)
httpAPIResponse.make(self, type: str='HTTP/2.0') -> str

# HttpRedirect inherits from HttpResponse
HttpRedirect(self, location: str)
```

```python
Request(self, http_data: str, client_address: tuple[str, int])
```
