import asyncio
import websockets
import logging
from websockets import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()
    counter = 0

    async def periodic_message(self, period: int):
        while True:
            await asyncio.sleep(period)
            if self.clients:
                await self.send_2_clients(f'hello world {self.counter}')
                logging.info(f'periodic message sent {self.counter} times')
                self.counter += 1

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
            if 'ignore' in message:
                logging.info('there is ignore word in the message')
            else:
                await self.send_2_clients(message)

    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str):
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)


server = Server()
start_srv = websockets.serve(server.ws_handler, 'localhost', 4000)
loop1 = asyncio.get_event_loop()
loop2 = asyncio.get_event_loop()
loop1.run_until_complete(start_srv)
loop2.run_until_complete(server.periodic_message(5))
loop1.run_forever()
loop2.run_forever()
