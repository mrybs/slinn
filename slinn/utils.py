import re, threading, socket, inspect


class StoppableThread(threading.Thread):
    def __init__(self,  *args: tuple, **kwargs: dict):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def optional(func, *args, **kwargs):
	_args, _kwargs, k= [], {}, {}
	s = str(inspect.signature(func))[1:-1].split(',')
	for key in kwargs.keys():
		if key in s:
			k[key] = kwargs[key]
	kwargs = k
	if len(s) < len(args):
		_args = args[:-len(s)]
	elif len(s) < len(args) + len(kwargs):
		_args, _kwargs = args[:-len(s)], {list(kwargs.keys())[i]: kwargs[list(kwargs.keys())[i]] for i in range(len(kwargs)-len(s)-len(args))}
	else:
		_args, _kwargs = args, kwargs
	func(*_args, **_kwargs)

def restartswith(text: str, reg: str):
	buf, largest = '', None
	for c in text:
		buf += c
		if re.sub(reg, '', buf) == '':
			largest = buf
	return largest is not None

def rematcheswith(text: str, reg: str): 
	return re.match('^'+reg+'$', text) is not None

def Bmin_restartswith_size(text: str, reg: str):
	buf, smallest = text, None
	for _ in range(len(text)):
		buf = buf[:-1]
		if re.sub(reg, '', buf) == '':
			smallest = buf
		else:
			break
	return len(smallest) if smallest is not None else 2147483647

def min_restartswith_size(text: str, reg: str):
	buf, smallest = text, None
	for _ in range(len(text)):
		buf = buf[:-1]
		if re.sub(reg, '', buf) == '':
			smallest = buf
	return len(smallest) if smallest is not None else 2147483647

def check_socket(sock):
	return sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) == 0
