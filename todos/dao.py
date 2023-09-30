# отдельный файл для работы с БД // DAO - data acces object
from datetime import date

from sqlalchemy import select, delete

from src.dao.base import BaseDAO # Базовый класс для работы с БД
from src.database import async_session_maker, engine
# from app.database import async_session_maker, engine  # импортируем генератор сессий
# from sqlalchemy import select, insert, func, and_, or_
# from app.bookings.models import Bookings
# from app.hotels.rooms.models import Rooms


# BookingDAO.find_all() - Обращение
from src.todos.models import Todos


class TodosDAO(BaseDAO):

    model = Todos

    @classmethod
    async def find_all_from_param(cls,  **filter_by):
        async with async_session_maker() as session:  # используем асинхронный контекстный менеджер
            # если произойдёт ошибка - сессия всегда закроется
            #query = select(cls.model)  # SELECT * FROM bookings
            query = select(cls.model).filter_by(**filter_by) # (user_id = 1, price = 24500)

            result = await session.execute(query)  # Исполняем наш запрос и получим // <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x7f242a738a40>
            # print(bookings) # .one - первая запись, .all - все записи
            # print(bookings.all()) # [(<app.bookings.models.Bookings object at 0x7ffa1b10dc90>,), (<app.bookings.models.Bookings object at 0x7ffa1b10dc30>,)] // можем использовать дальше: джоинить и т.д.
            # print(bookings.scalars().all()) # [<app.bookings.models.Bookings object at 0x7f32f7a09c90>, <app.bookings.models.Bookings object at 0x7f32f7a09c30>]
            # scalars можно вызывать только один раз, поэтому, если нужен принт - надо сохранить его в переменную
            return result.scalars().all()  # Вернёт уже JSON, т.к. FastAPI всегда пытается конвертировать ответ в JSON


    @classmethod
    async def delete(cls, **filter_by):  # Удаление чего-то
        async with async_session_maker() as session:  # используем асинхронный контекстный менеджер
            query = delete(cls.model).filter_by(**filter_by)
            print(query.compile(engine, compile_kwargs={'literal_binds': True})) # Чтобы увидеть сырой запрос
            # DELETE FROM bookings WHERE bookings.id = 2 AND bookings.user_id = 4
            # compile - скомпилируй, engine - наш движок, compile_kwargs - необходимые аргументы для компиляции

            await session.execute(query) # исполняем запрос
            await session.commit() # фиксируем все изменения










