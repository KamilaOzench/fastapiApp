# Модели SQLAlchemy

from sqlalchemy import Column, Date, Integer, String, JSON, SMALLINT, ForeignKey, Computed, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from src.database import Base

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, nullable=False)
    owner = Column(ForeignKey('users.id'), nullable=False)
    text = Column(String, nullable=False)
    date_start = Column(Date, nullable=False)
    date_stop = Column(Date, nullable=False)
    success = Column(Boolean, nullable=False, default=False)







