from slinn import AsyncServer, Response, Address, ResponseHeader, ResponseChunk, ApiDispatcher, SSEHeader, SSEEvent
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


@dp.get('sse')
async def sse(request):
    await request.respond(SSEHeader, '*')
    while True:
        await request.respond(SSEEvent, full_data=['lolkek'], event_id=1488, retry=500, comments=['alikhan daun eblan'], event='да по жизни так')
        await asyncio.sleep(1)


asyncio.run(AsyncServer(dp).listen(Address(8080)))
