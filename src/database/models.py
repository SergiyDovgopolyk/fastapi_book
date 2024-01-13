from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from .db import engine  # Оновлено імпорт

class Base(DeclarativeBase):
    pass

# Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    birth_date = Column(Date)
    additional_data = Column(String, nullable=True)