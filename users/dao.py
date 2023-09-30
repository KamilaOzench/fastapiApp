# отдельный файл для работы с БД // DAO - data acces object
from datetime import date

from sqlalchemy import select, and_

from src.dao.base import BaseDAO # Базовый класс для работы с БД
from src.database import async_session_maker

from src.users.models import Users
from src.todos.models import Todos



class UsersDAO(BaseDAO):

    # Методы обращения к таблице

    model = Users



    @classmethod
    async def get_todo(cls, user_id: int):
        '''SELECT users."id" AS users_id, users."name", users.email,
        todos."id" AS todos_id, todos.text, todos.date_start, todos.date_stop, todos.success
        FROM users
        JOIN todos ON users."id" = todos."owner" '''


        async with async_session_maker() as session:
            query = (
                select(
                        Users.id,
                        Users.name,
                        Users.email,

                        Todos.id,
                        Todos.text,
                        Todos.date_start,
                        Todos.date_stop,
                        Todos.success,

                        ).select_from(Users).join(Todos, Users.id == Todos.owner)
            .where(and_(
                    and_(Todos.date_start < Todos.date_stop),
                    and_(Users.id == user_id)
                )
                )

            )

            result = await session.execute(query)
            return result.all()










