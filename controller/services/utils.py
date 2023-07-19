import asyncio
from datetime import timedelta

from controller.config import settings
from controller.db.postgres import Controller
from controller.schemas import AllControllersGetReponse


async def get_controller_status_by_payload(payload: int) -> str:
    return "UP" if payload % 2 == 0 else "DOWN"


async def sort_controllers_by_datetime(
    controllers: list[Controller]
) -> list[Controller]:
    return sorted(controllers, key=lambda x: x.datetime)


async def combine_controllers_interval_with_same_status(
    controllers: list[Controller]
) -> list[AllControllersGetReponse]:
    resp: list[AllControllersGetReponse] = []

    sorted_controllers = await sort_controllers_by_datetime(controllers)

    for control in sorted_controllers:
        if len(resp) == 0 or resp[-1].status != control.status:
            resp.append(
                AllControllersGetReponse(
                    datetime_start=control.datetime,
                    datetime_end=control.datetime + timedelta(
                        seconds=settings.INTERVAL
                    ),
                    status=control.status,
                )
            )
            continue

        resp[-1].datetime_end = control.datetime + timedelta(
            seconds=settings.INTERVAL
        )

    return resp


async def message_handling() -> bool:
    await asyncio.sleep(5)
    return True
