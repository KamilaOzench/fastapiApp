# Базовый класс для работы с БД

from src.database import async_session_maker, engine
from sqlalchemy import select, insert, delete


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            # looking for a certain id
            result = await session.execute(query)
            return result.scalar_one_or_none()



    @classmethod
    async def find_one_or_none(cls, **filter_by): # id=1, name='Ivan'
        # Ckecking whether the user is registered
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by) # id=1, name='Ivan'
            result = await session.execute(query)
            return result.scalar_one_or_none()
            # Here is a special method of Alchemy // we get either one object or None





    @classmethod
    async def find_all(cls,  **filter_by):
        async with async_session_maker() as session:

            query = select(cls.model).filter_by(**filter_by) # (user_id = 1, price = 24500)

            result = await session.execute(query)  # Исполняем наш запрос и получим // <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x7f242a738a40>
            # print(bookings) # .one - первая запись, .all - все записи
            # print(bookings.all()) # [(<app.bookings.models.Bookings object at 0x7ffa1b10dc90>,), (<app.bookings.models.Bookings object at 0x7ffa1b10dc30>,)] // можем использовать дальше: джоинить и т.д.
            # print(bookings.scalars().all()) # [<app.bookings.models.Bookings object at 0x7f32f7a09c90>, <app.bookings.models.Bookings object at 0x7f32f7a09c30>]
            # scalars можно вызывать только один раз, поэтому, если нужен принт - надо сохранить его в переменную
            return result.scalars().all()  # Вернёт уже JSON, т.к. FastAPI всегда пытается конвертировать ответ в JSON


    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)#.returning(cls.model.id) # INSERT INTO VALUES  /// return id
            await session.execute(query)  # Исполняем наш запрос и получим // <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x7f242a738a40>
            await session.commit()

    @classmethod
    async def delete(cls, **filter_by):  # Удаление чего-то
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            print(query.compile(engine, compile_kwargs={'literal_binds': True})) # Чтобы увидеть сырой запрос
            # DELETE FROM bookings WHERE bookings.id = 2 AND bookings.user_id = 4
            # compile - скомпилируй, engine - наш движок, compile_kwargs - необходимые аргументы для компиляции

            await session.execute(query) # исполняем запрос
            await session.commit() # фиксируем все изменения

