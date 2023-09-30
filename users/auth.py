from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from pydantic import EmailStr



from src.config import settings
from src.users.dao import UsersDAO

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    # Tutorial -> Security -> OAuth2 with Password (and hashing), Bearer with JWT tokens
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



async def authentificate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email) # Проверяем, есть ли такой пользователь
    if not user and not verify_password(password, user.hashed_password):
        return None
    return user




def create_access_token(data: dict) -> str: # Принимает словарь и возвращает JWT(str)
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30) # текущее время в utc формате + 30 минут // время когда истечёт токен доступа (есть езё рефреш токен - долгосрочный)
    to_encode.update({'exp': expire}) # Добавляем значение в словарь
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM) # Пояснения в JWT.jwt
    return encoded_jwt


