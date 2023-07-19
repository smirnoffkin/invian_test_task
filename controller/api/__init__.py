from fastapi import APIRouter

from . import controller, ping

main_api_router = APIRouter()

main_api_router.include_router(controller.router)
main_api_router.include_router(ping.router)
