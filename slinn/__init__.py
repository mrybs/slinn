import sys
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
from slinn.http_response import HttpResponse
from slinn.http_redirect import HttpRedirect
from slinn.empty_http_response import EmptyHttpResponse
from slinn.http_render import HttpRender
from slinn.http_api_response import HttpAPIResponse
from slinn.http_json_response import HttpJSONResponse
from slinn.http_json_api_response import HttpJSONAPIResponse
from slinn.server import Server
from slinn import utils


VERSION = {
    'name': 'Slinn',
    'codename': 'Nukeful',
    'version': '2.3.1',
    'version_id': '060425B',
    'dies_at': datetime(2025, 6, 6, 23, 59)
}
version = '{} {} v{} {}'.format(*list(VERSION.values())[:-1])

Response = HttpResponse
Redirect = HttpRedirect
EmptyResponse = EmptyHttpResponse
Render = HttpRender
APIResponse = HttpAPIResponse
JSONResponse = HttpJSONResponse
JSONAPIResponse = HttpJSONAPIResponse

HttpResponse = utils.make_deprecated(HttpResponse, 'Response')
HttpRedirect = utils.make_deprecated(HttpRedirect, 'Redirect')
EmptyHttpResponse = utils.make_deprecated(EmptyHttpResponse, 'EmptyResponse')
HttpRender = utils.make_deprecated(HttpRender, 'Render')
HttpAPIResponse = utils.make_deprecated(HttpAPIResponse, 'APIResponse')
HttpJSONResponse = utils.make_deprecated(HttpJSONResponse, 'JSONResponse')
HttpJSONAPIResponse = utils.make_deprecated(HttpJSONAPIResponse, 'JSONAPIResponse')

if datetime.now() > VERSION['dies_at']:
    exit("Slinn`s version has expired. You need to upgrade")
