# Модели SQLAlchemy

from sqlalchemy import Column, Date, Integer, String, JSON, SMALLINT, ForeignKey, Computed
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from src.database import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)





