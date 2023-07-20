import asyncio
from logging import getLogger
from typing import Any

logger = getLogger(__name__)


class Manipulator:
    @staticmethod
    def add_log(event: Any):
        logger.error(event)


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        Manipulator.add_log('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        Manipulator.add_log('Data received: {!r}'.format(message))

        Manipulator.add_log('Send: {!r}'.format(message))
        self.transport.write(data)

        Manipulator.add_log('Close the client socket')
        self.transport.close()


async def run_server():
    loop = asyncio.get_running_loop()
    host = '127.0.0.1'
    port = 8888

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        host, port
    )

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(run_server())
