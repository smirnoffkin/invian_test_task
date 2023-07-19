from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from controller.db.postgres import get_db
from controller.schemas import (
    InputControllerRequest,
    InputControllerResponse,
    ControllerGetResponse,
    AllControllersGetReponse
)
from controller.services import (
    _create_new_controller,
    _delete_controller_by_date,
    _get_controller_by_date,
    _get_all_controllers
)

router = APIRouter(prefix="/controller", tags=["Controller"])


@router.post(
    "/",
    description="Create controller",
    response_model=InputControllerResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_controller(
    body: InputControllerRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        new_controller = await _create_new_controller(body, db)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This controller is already exists"
        )
    except DBAPIError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check timezone at datetime"
        )
    return {
        "success": True,
        "datetime": new_controller.datetime,
        "payload": body.payload
    }


@router.get(
    "/{date}",
    description="Get controller by date",
    response_model=ControllerGetResponse,
    status_code=status.HTTP_200_OK
)
@cache(expire=10)
async def get_controller_by_date(
    date: datetime = datetime.now(),
    db: AsyncSession = Depends(get_db)
):
    controller = await _get_controller_by_date(date, db)
    if controller is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Controller not found."
        )
    return controller


@router.get(
    "/all/",
    description="Get a list of all controllers",
    response_model=list[AllControllersGetReponse],
    status_code=status.HTTP_200_OK
)
@cache(expire=5)
async def get_all_controllers(db: AsyncSession = Depends(get_db)):
    return await _get_all_controllers(db)


@router.delete(
    "/{date}",
    description="Delete controller by date",
    response_model=ControllerGetResponse,
    status_code=status.HTTP_200_OK
)
async def delete_controller(
    date: datetime = datetime.now(),
    db: AsyncSession = Depends(get_db)
):
    controller_to_delete = await _get_controller_by_date(date, db)
    if controller_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Controller not found."
        )
    deleted_controller = await _delete_controller_by_date(date, db)
    return deleted_controller
