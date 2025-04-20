import sys
import warnings
from datetime import datetime
from slinn.address import Address
from slinn.handle import Handle
from slinn.i_middleware import IMiddleware
from slinn.filter import Filter
from slinn.link_filter import LinkFilter
from slinn.any_filter import AnyFilter
from slinn.file import File
from slinn.preprocessor import Preprocessor
from slinn.dispatcher import Dispatcher
from slinn.hcdispatcher import HCDispatcher
from slinn.ftdispatcher import FTDispatcher
from slinn.request import Request
from slinn.async_request import AsyncRequest
from slinn.http_response import HttpResponse
from slinn.http_response_header import HttpResponseHeader
from slinn.http_response_chunk import HttpResponseChunk
from slinn.http_redirect import HttpRedirect
from slinn.empty_http_response import EmptyHttpResponse
from slinn.http_render import HttpRender
from slinn.http_api_response import HttpAPIResponse
from slinn.http_json_response import HttpJSONResponse
from slinn.http_json_api_response import HttpJSONAPIResponse
from slinn.sse_header import SSEHeader
from slinn.sse_event import SSEEvent
from slinn.websocket_opcodes import WebSocketOpcodes
from slinn.websocket_handshake import WebSocketHandshake
from slinn.websocket_frame import WebSocketFrame
from slinn.async_websocket_connection import AsyncWebSocketConnection
from slinn.server import Server
from slinn.async_server import AsyncServer
from slinn.api_dispatcher import ApiDispatcher
from slinn import utils


VERSION = {
    'name': 'Slinn',
    'codename': 'Nukeful',
    'version': '2.3.1',
    'version_id': '210425A',
    'dies_at': datetime(2025, 6, 18, 23, 59)
}
version = '{} {} v{} {}'.format(*list(VERSION.values())[:-1])

Response = HttpResponse
ResponseHeader = HttpResponseHeader
ResponseChunk = HttpResponseChunk
Redirect = HttpRedirect
EmptyResponse = EmptyHttpResponse
Render = HttpRender
APIResponse = HttpAPIResponse
JSONResponse = HttpJSONResponse
JSONAPIResponse = HttpJSONAPIResponse

HttpResponse = utils.make_deprecated(HttpResponse, Response)
HttpRedirect = utils.make_deprecated(HttpRedirect, Redirect)
EmptyHttpResponse = utils.make_deprecated(EmptyHttpResponse, EmptyResponse)
HttpRender = utils.make_deprecated(HttpRender, Render)
HttpAPIResponse = utils.make_deprecated(HttpAPIResponse, APIResponse)
HttpJSONResponse = utils.make_deprecated(HttpJSONResponse, JSONResponse)
HttpJSONAPIResponse = utils.make_deprecated(HttpJSONAPIResponse, JSONAPIResponse)

warnings.simplefilter('always', DeprecationWarning)

if datetime.now() > VERSION['dies_at']:
    exit("Slinn`s version has expired. You need to upgrade")
