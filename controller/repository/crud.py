from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from controller.db.postgres import Controller


class ControllerCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_controller(
        self,
        date: datetime,
        status: str
    ) -> Controller:
        new_controller = Controller(datetime=date, status=status)
        self.db_session.add(new_controller)
        await self.db_session.commit()
        return new_controller

    async def get_controller_by_date(
        self,
        date: datetime
    ) -> Controller | None:
        query = select(Controller).where(Controller.datetime == date)
        res = await self.db_session.execute(query)
        post_row = res.fetchone()
        if post_row is not None:
            return post_row[0]

    async def get_all_controllers(self) -> list:
        query = select(Controller)
        res = await self.db_session.execute(query)
        posts = list(res.scalars().all())
        return posts

    async def delete_controller_by_date(
        self,
        date: datetime
    ) -> Controller | None:
        query = (
            delete(Controller)
            .where(Controller.datetime == date)
            .returning(Controller)
        )
        res = await self.db_session.execute(query)
        deleted_post_row = res.fetchone()
        if deleted_post_row is not None:
            return deleted_post_row[0]
