import asyncio
from datetime import datetime

import sys

from sqlalchemy.ext.asyncio import AsyncSession

from controller.db.postgres import Controller
from controller.repository import ControllerCRUD
from controller.schemas import InputControllerRequest
from controller.services.utils import (
    combine_controllers_interval_with_same_status,
    get_controller_status_by_payload,
    message_handling
)
from manipulator import send_message_to_manipulator

sys.path.append("..")


async def _create_new_controller(
    body: InputControllerRequest,
    db: AsyncSession
) -> Controller:
    # TODO sort out the connection with the manipulator
    # event_to_decide = asyncio.create_task(message_handling())
    # if event_to_decide:
    #     await send_message_to_manipulator(
    #         f"Successfully added new controller: {body}"
    #     )

    async with db.begin():
        status = await get_controller_status_by_payload(body.payload)

        controller_crud = ControllerCRUD(db)
        return await controller_crud.create_controller(
            date=body.datetime,
            status=status
        )


async def _get_controller_by_date(
    date: datetime,
    db: AsyncSession
) -> Controller | None:
    async with db.begin():
        controller_crud = ControllerCRUD(db)
        return await controller_crud.get_controller_by_date(date)


async def _get_all_controllers(db: AsyncSession) -> list:
    async with db.begin():
        controller_crud = ControllerCRUD(db)
        controllers = await controller_crud.get_all_controllers()
        controllers = await combine_controllers_interval_with_same_status(
            controllers
        )
        return controllers


async def _delete_controller_by_date(
    date: datetime,
    db: AsyncSession
) -> Controller | None:
    async with db.begin():
        controller_crud = ControllerCRUD(db)
        return await controller_crud.delete_controller_by_date(date)
