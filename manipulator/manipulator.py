import asyncio
import socket
from logging import getLogger
from typing import Any

logger = getLogger(__name__)


class Manipulator:
    @staticmethod
    async def add_log(event: Any):
        logger.error(event)


async def server_program():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    await Manipulator.add_log(f"Successfully started tcp server on port :{port}")

    conn, address = server_socket.accept()
    await Manipulator.add_log("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if data:
            await Manipulator.add_log("from connected user: " + str(data))
            conn.send(data.encode())


if __name__ == '__main__':
    asyncio.run(server_program())
