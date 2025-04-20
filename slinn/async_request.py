from slinn import Request, utils
import asyncio


class AsyncRequest(Request):
    """
    Representation of HTTP request from client
    """

    def __init__(self, loop, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.loop = loop

    async def respond(self, response_class, *args, **kwargs) -> None:
        made = utils.optional(response_class(*args, **kwargs).make, version = self.version, htrf = self.htrf)
        if made is None:
            return
        await self.loop.sock_sendall(self.connection, made)

    async def recv(self, n_bytes: int) -> bytes:
        return await self.loop.sock_recv(self.connection, n_bytes)
