import asyncio
import socket
from typing import Any

from .manipulator import Manipulator


async def send_message_to_manipulator(message: Any = ""):
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    while True:
        try:
            client_socket.send(message.encode())
            data = client_socket.recv(1024).decode()

            await Manipulator.add_log('Received from server: ' + data)
        except KeyboardInterrupt:
            client_socket.close()
            break
        finally:
            client_socket.close()
            break


if __name__ == "__main__":
    asyncio.run(send_message_to_manipulator())
