from __future__ import annotations
from slinn import Request, Address, Filter, Logger, LogLevel, HCDispatcher, utils
import socket, ssl, os, traceback


RED = '\u001b[31m'
RESET = '\u001b[0m'


class Server:
    """
    Main class to start server
    """
    class Handle:
        def __init__(self, filter: Filter, function):
            self.filter = filter
            self.function = function

    def __init__(self, *dispatchers: tuple[Dispatcher, ...], smart_navigation: bool = True, ssl_fullchain: str = None, # type: ignore
                 ssl_key: str = None, timeout: float = 0.03, max_bytes_per_recieve: int = 4096,
                 max_bytes: int = 4294967296, _func=lambda server: None, logger: Logger = Logger(LogLevel.warning),
                 ecdp: HCDispatcher = HCDispatcher()) -> None:
        self.dispatchers = dispatchers
        self.smart_navigation = smart_navigation
        self.server_socket = None
        self.ssl = ssl_fullchain is not None and ssl_key is not None
        self.ssl_cert, self.ssl_key = ssl_fullchain, ssl_key
        self.ssl_context = None
        self.thread = None
        self.timeout = timeout
        self.max_bytes_per_recieve = max_bytes_per_recieve
        self.max_bytes = max_bytes
        self._func = _func
        self.logger = logger
        self.ecdp = ecdp

    def reload(self, *dispatchers: tuple) -> None:
        if self.thread is not None:
            self.thread.stop()
            try:
                self.thread.join()
            except RuntimeError:
                pass
        self.dispatchers = dispatchers
        self.logger(LogLevel.info, 'Server has reloaded')

    def address(self, port: int, domain: str=None):
        protocol = 'https' if self.ssl else 'http'
        return (f'{protocol.upper()} server is available on {protocol}://'+
               ('0.0.0.0' if (domain is None or domain == '') else ('['+domain+']' if ':' in domain else domain))+
               f'{(":"+str(port) if port != 443 else "") if self.ssl else (":"+str(port )if port != 80 else "")}/')

    def listen(self, address: Address):
        self.server_socket = None
        if ':' in address.host:
            self.server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            if socket.has_dualstack_ipv6():
                self.server_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        else:
            self.server_socket = socket.socket(socket.AF_INET if '.' in address.host else socket.AF_INET6,
                                               socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((address.host, address.port))
        except PermissionError:
            if not self.logger(LogLevel.critical, 'Permission denied'):
                print(f'{RED}Permission denied{RESET}')
            exit(13)
        if self.ssl:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ssl_context.load_cert_chain(certfile=self.ssl_cert, keyfile=self.ssl_key)
        self.server_socket.settimeout(self.timeout)
        self.server_socket.listen()
        self.logger(LogLevel.info, 'Server started to listening')
        print(self.address(address.port, address.domain))
        try:
            while True:
                try:
                    utils.StoppableThread(target=self.handle_request, args=self.server_socket.accept()).start()
                except socket.timeout:
                    pass
        except KeyboardInterrupt:
            print('Got KeyboardInterrupt, halting the application...')
            if utils.check_socket(self.server_socket):
                self.server_socket.close()
            os._exit(0)

    def handle_request(self, client_socket, client_address):
        try:
            self._func(self)
            if self.ssl:
                client_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)
            request: Request
            try:
                client_socket.settimeout(self.timeout)
                data = bytearray()
                while len(data) < self.max_bytes:
                    try:
                        b = client_socket.recv(self.max_bytes_per_recieve)
                        data += b
                    except TimeoutError:
                        break

                data = data.split(b'\r\n\r\n')
                header = data[0].decode()
                content = b'\r\n\r\n'.join(data[1:])

                if header == '':
                    return
                request = Request(header, content, client_address, client_socket)
                self.logger(LogLevel.info, repr(request))
            except KeyError:
                return self.logger(LogLevel.info, 'Got KeyError, probably invalid request. Ignore')
            except UnicodeDecodeError:
                return self.logger(LogLevel.info, 'Got UnicodeDecodeError, probably invalid request. Ignore')
            except ConnectionResetError:
                return self.logger(LogLevel.info, 'Connection reset by client')
            except OSError:
                return self.logger(LogLevel.info, 'Connection closed')
            for dispatcher in self.dispatchers:
                if True in [utils.restartswith(request.host, host) for host in dispatcher.hosts]:
                    if self.smart_navigation:
                        sizes = [handle.filter.size(request.link, request.method) for handle in dispatcher.handles]
                        if sizes != []:
                            if self.answer_request(client_socket, dispatcher.handles[sizes.index(max(sizes))], request,
                                                   data, header, content):
                                return
                    else:
                        for handle in dispatcher.handles:
                            if self.answer_request(client_socket, handle, request, data, header, content):
                                return
        except Exception as exception:
            self.logger(LogLevel.warning, f'During handling request, an {exception} has occured')
            self.logger(LogLevel.warning, traceback.extract_stack())
            self.reload(*self.dispatchers)

    def answer_request(self, client_socket, handle, request, http_data, http_header, http_content):
        if handle.filter.check(request.link, request.method):
            if utils.check_socket(client_socket):
                response = utils.optional(handle.function,
                                          request=request,
                                          http_data=http_data,
                                          http_header=http_header,
                                          http_content=http_content,
                                          client_socket=client_socket)
                if type(response) is int:
                    if response < 99 or response > 599:
                        raise ValueError(f'Error code {response} does not exist')
                    handle = self.ecdp(response)
                    if handle is not None:
                        return self.answer_request(client_socket, handle, request, http_data, http_header, http_content)
                    self.logger(LogLevel.error, f'Error code {response} `s handler is not defined')
                elif response is not None:
                    client_socket.sendall(utils.optional(response.make, type=request.version, gzip=True))
                client_socket.close()
            return True
        return False
