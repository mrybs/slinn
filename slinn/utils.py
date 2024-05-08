import re, threading, socket, inspect, json


class StoppableThread(threading.Thread):
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    def stopped(self) -> bool:
        return self._stop_event.is_set()


def optional(func, *args, **kwargs) -> any:
    _args, _kwargs, k = [], {}, {}
    s = [arg.split(':')[0] for arg in ')'.join('('.join(str(inspect.signature(func)).split('(')[1:]).split(')')[:-1]).split(',')]
    for key in kwargs.keys():
        if key in s:
            k[key] = kwargs[key]
    kwargs = k
    if len(s) < len(args):
        _args = args[:-len(s)]
    elif len(s) < len(args) + len(kwargs):
        _args, _kwargs = args[:-len(s)], {list(kwargs.keys())[i]: kwargs[list(kwargs.keys())[i]] for i in
                                          range(len(kwargs) - len(s) - len(args))}
    else:
        _args, _kwargs = args, kwargs
    return func(*_args, **_kwargs)


def restartswith(text: str, reg: str) -> bool:
    buf, largest = '', None
    for c in text:
        buf += c
        if re.sub(reg, '', buf) == '':
            largest = buf
    return largest is not None


def rematcheswith(text: str, reg: str) -> bool:
    return re.match('^' + reg + '$', text) is not None


def Bmin_restartswith_size(text: str, reg: str) -> int:
    buf, smallest = text, None
    for _ in range(len(text)):
        buf = buf[:-1]
        if re.sub(reg, '', buf) == '':
            smallest = buf
        else:
            break
    return len(smallest) if smallest is not None else 2147483647


def min_restartswith_size(text: str, reg: str) -> int:
    buf, smallest = text, None
    for _ in range(len(text)):
        buf = buf[:-1]
        if re.sub(reg, '', buf) == '':
            smallest = buf
    return len(smallest) if smallest is not None else 2147483647


def check_socket(sock) -> bool:
    return sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) == 0

def representate(obj: any) -> str:
    if type(obj) == dict:
        return json.dumps({key:representate(obj[key]) for key in obj.keys()})
    if type(obj) in [list, tuple, set]:
        return ', '.join([representate(elem) for elem in obj])
    if type(obj) == str:
        return obj
    if type(obj) == bytes:
        return obj.decode()
    if type(obj) in [int, float]:
        return str(obj)
    if type(obj) == bool:
        return 'true' if obj else 'false'
    if type(obj).__str__ != object.__str__ or type(obj).__repr__ != object.__repr__:
        try: return str(obj)
        except Exception: pass
    try: return json.dumps({key:representate(obj.__dict__[key]) for key in obj.__dict__.keys()})
    except Exception as e: print(e)
    return f'<{type(obj)} object at {id(obj)}>'
