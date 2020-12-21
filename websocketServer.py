import asyncio
import websockets
import logging
from websockets import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connected')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnected')

    async def send_2_clients(self, message: str):
        await asyncio.wait([client.send(message) for client in self.clients])

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            await self.send_2_clients(message)

    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str):
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)


server = Server()
start_srv = websockets.serve(server.ws_handler, 'localhost', 4000)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_srv)
logging.info('server started')
loop.run_forever()
