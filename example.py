from slinn import AsyncServer, AnyFilter, Response, Address, LinkFilter, ResponseHeader, ResponseChunk, ApiDispatcher
import logging
import os
import asyncio


logging.basicConfig(level=logging.INFO)
dp = ApiDispatcher()


@dp.get()
async def index(request):
    await request.respond(Response, 'Hello, world')


@dp.get('gpsl')
async def gpsl(request):
    await request.respond(ResponseHeader, [('Content-Length', os.path.getsize(r'C:\Users\mrybs\Downloads\ГПсЛ.zip'))])

    with open(r'C:\Users\mrybs\Downloads\ГПсЛ.zip', 'rb') as f:
        i = 1
        while data := f.read(1024*64):
            await request.respond(ResponseChunk, data)
            await asyncio.sleep(0)
            i += 1


asyncio.run(AsyncServer(dp).listen(Address(8080)))
