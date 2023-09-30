from fastapi import APIRouter, Response, Depends

from src.users.auth import get_password_hash, authentificate_user, create_access_token
from src.users.dao import UsersDAO
from src.users.dependencies import get_current_user
from src.users.schemas import Users, SUserAuth

router = APIRouter(
    prefix='/users',
    tags=['Пользователи'],
)



@router.post('/register')
async def register_user(user_data: SUserAuth): # Функция регистрации пользователей
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        return None
        # raise UserAlreadyExistsException # Если по данному email уже есть регистрация то будет 500 ошибка
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    return {'message': 'success'}


@router.post('/login')
async def login(response: Response, user_data: SUserAuth):# -> Users: # -> валидация на выходе
    user = await authentificate_user(email=user_data.email, password=user_data.password)
    data = {'sub': str(user.id)}
    token = create_access_token(data)

    response.set_cookie('todo_cookie', token, httponly=True, secure=True)
    # засетим cookie //
    # название, токен, важный параметр безопасности чтобы токен нельзя было воспроизвести через JS
    return token  # на самом деле, можем вернуть всё что угодно, токен мы уже засетили
    # return {'access_token': access_token, 'refresh_token': refresh} # Чаще всего возвращают так


@router.get('/me') # Пользователь получает информацию о себе
async def read_users_me(current_user: Users = Depends(get_current_user)):
    # Т.к. есть Depends - всё проходит по циклу зависимостей
    return current_user.email


@router.get('get_todos/')
async def get_todos(id:int):
    todos = await UsersDAO.get_todo(user_id=id)
    return todos