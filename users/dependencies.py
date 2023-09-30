# Зависимости для проверки, аутентифицирован ли пользователь
from datetime import datetime

from fastapi import Request, Depends, HTTPException  # Необходимо чтобы распарсить информацию о токенах из запроса
from jose import jwt, JWTError

from src.config import settings
# from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, \
#     UserIsNotPresentException
from src.users.dao import UsersDAO
from src.users.models import Users


def get_token(request: Request): # Получение cookies //
    token = request.cookies.get('todo_cookie') # Проверяем, есть ли такой ключ
    if not token:
        # print(request.cookies)
        raise HTTPException(status_code=500)
        # raise TokenAbsentException # Токен отсутствует
    return token
 # 1) Нужная кука booking_access_token отправлена вместе с запросом




async def get_current_user(token: str = Depends(get_token)): # Достаём user из cookies // Depends - зависит от...
    'Request в FastAPI существует только в рамках одного запроса, поэтому, необходимо применять Depends, а не переменную'
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        # Декодируем наш JWT токен

    except JWTError:
        raise HTTPException(status_code=500)
        # Некорректный формат токена

    expire: str = payload.get('exp') # Получаем дату истечения
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=500)
        # TokenExpiredException # Токен истёк

    user_id: str = payload.get('sub') # Получаем id пользователя
    if not user_id:
        raise HTTPException(status_code=500)
        # raise UserIsNotPresentException # Без комментариев, в целях безопасности>

    print(user_id, type(user_id)) # 4 // <class 'str'>
    user = await UsersDAO.find_by_id(int(user_id)) # Используем функцию для поиска юзера

    if not user:
        raise HTTPException(status_code=500)
        # raise UserIsNotPresentException # Без комментариев, в целях безопасности>

    return user # Лучше создать отдельно метод чтобы возвращать без пароля

 # 2) В куке содержится не абы какая строка, а JWT токен
 # 3) JWT токен все еще живой, дата экспирации не прошла
 # 4) В токене есть необходимые поля с данными пользователя
 # 5) Пользователь с таким id существует в БД
 # 6) Возвращение данных о пользователе: id, email, имя, фамилия и т.п.


async def get_current_admin_user(current_user: Users = Depends(get_current_user)): # Проверка на роль админа
    # if current_user.role != 'admin':  # Комментируем чтобы не прописывать роли в бд
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not role')
    return current_user
