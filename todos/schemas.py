# pydantic схемы

from datetime import date
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class Todos(BaseModel):
    #id: int
    owner: int
    text: str
    date_start: date
    date_stop: date
    #success: bool

    class Config: # нужно чтобы pydantic распознал схему алхимии
        # // смотри на нашу модель не только как словарь, но и на класс у которого есть аттрибуты
        orm_mode = True












#
# class SBookings(BaseModel):
#     id: int
#     room_id: int
#     user_id: int
#     date_from: date
#     date_to: date
#     price: int
#     total_cost: int
#     total_days: int
#
#     # class Config: # нужно чтобы pydantic распознал схему алхимии  (1.6 последнее видео) // смотри на нашу модель не только как словарь, но и на класс у которого есть аттрибуты
#     #     orm_mode = True
#
# class SBookingsInfo(SBookings):
#     image_id: int
#     name: str
#     description: Optional[str]
#     services: List[str]
#     #
#     # class Config:
#     #     orm_mode = True