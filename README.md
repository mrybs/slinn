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
from slinn import Server, Dispatcher, Filter, HttpResponse, Address


dp = Dispatcher()


@dp.route(Filter('/api.*'))
def api(request):
    return HttpAPIResponse('{"status": "ok"}')


@dp.route(Filter('.*'))
def helloworld(request):
     return HttpResponse('Hello world!')

# The following code is not required when using manage.py
app = Server(dp, ssl_cert='fullchain.pem', ssl_key='key.pem')
app.listen(Address(8080))

```

#### Functions:
```python
Server(self, *dispatchers, ssl_cert: str=None, ssl_key: str=None, http_ver: str='2.0')
Server.listen(self, address: Address)
```

```python
Address(self, port: int, host: str=None)
```

```python
Dispatcher(self, hosts: list=None)
Dispatcher.route(self, filter: Filter)
```

```python
Filter(self, filter: str, methods: list[str]=None)
Filter.check(self, text: str, method: str) -> bool
```

```python
HttpResponse(self, payload, data: list[tuple]=None, status: str='200 OK', content_type: str='text/plain')
HttpResponse.set_cookie(self, key: str, value)
HttpResponse.make(self, type: str='HTTP/2.0') -> str
```

```python
HttpAPIResponse(self, payload, data: list[tuple]=None, status: str='200 OK', content_type: str='text/plain')
HttpAPIResponse.set_cookie(self, key: str, value)
HttpAPIResponse.make(self, type: str='HTTP/2.0') -> str
```

HttpRedirect inherits from HttpResponse
```python
HttpRedirect(self, location: str)
```

```python
Request(self, http_data: str, client_address: tuple[str, int])
```
