import asyncio
from typing import Any

from .manipulator import Manipulator


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        transport.write(self.message.encode())
        Manipulator.add_log('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        Manipulator.add_log('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        Manipulator.add_log('The server closed the connection')
        self.on_con_lost.set_result(True)


async def send_signal_to_manipulator(message: Any = ""):
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()

    transport, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(message, on_con_lost),
        '127.0.0.1', 8888)

    try:
        await on_con_lost
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(send_signal_to_manipulator())
