from datetime import datetime as dt

from pydantic import BaseModel, validator


class BaseControllerSchema(BaseModel):
    datetime: dt
    payload: int

    def __str__(self) -> str:
        return f"datetime: {self.datetime}, payload: {self.payload}"

    class Config:
        orm_mode = True


class InputControllerRequest(BaseControllerSchema):
    @validator("datetime")
    def validate_datetime(cls, datetime: dt):
        return dt.strptime(str(datetime), "%Y-%m-%d %H:%M:%S")


class InputControllerResponse(BaseControllerSchema):
    success: bool = True


class ControllerGetResponse(BaseModel):
    datetime: dt
    status: str

    class Config:
        orm_mode = True


class AllControllersGetReponse(BaseModel):
    datetime_start: dt
    datetime_end: dt
    status: str

    class Config:
        orm_mode = True
