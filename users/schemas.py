# pydantic схемы

from datetime import date
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class Users(BaseModel):
    id: int
    name: Optional[str]
    email: EmailStr
    password: str


    class Config: # нужно чтобы pydantic распознал схему алхимии
        # // смотри на нашу модель не только как словарь, но и на класс у которого есть аттрибуты
        orm_mode = True



class SUserAuth(BaseModel):

    email: EmailStr
    password: str


    class Config: # нужно чтобы pydantic распознал схему алхимии
        # // смотри на нашу модель не только как словарь, но и на класс у которого есть аттрибуты
        orm_mode = True




