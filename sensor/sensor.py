import asyncio
import random
from datetime import datetime as dt

import aiohttp

COUNT_REQUEST_PER_SECOND = 300
COUNT_SENSORS = 8


async def get_random_controller_data() -> dict:
    datetime = dt.strftime(dt( \
        random.randint(2000, 2023), \
        random.randint(1, 12), \
        random.randint(1, 28), \
        random.randrange(23), \
        random.randrange(59), \
        random.randrange(59), \
        random.randrange(1000000)), '%Y-%m-%d %H:%M:%S')
    payload = random.randint(0, 100)

    return {"datetime": datetime, "payload": payload}


async def make_request():
    controller_data = await get_random_controller_data()
    async with aiohttp.ClientSession("http://localhost:8080") as session:
        async with session.post("/controller/", json=controller_data) as resp:
            print(resp.status)
            print(await resp.text())


async def main():
    async with asyncio.TaskGroup() as group:
        for _ in range(COUNT_REQUEST_PER_SECOND * COUNT_SENSORS):
            group.create_task(make_request())
            await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
