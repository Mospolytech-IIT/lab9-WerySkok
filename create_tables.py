"""
Часть 1: Подключение к базе данных и создание таблиц

Опишите модель данных, состоящую из двух таблиц: Users и Posts.

Напишите программу на Python, которая подключается к выбранной базе данных и создает таблицы Users и
Posts на основе описанной модели данных.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Users(Base):
    """
    Таблица Users должна содержать следующие поля:

    id (целое число, первичный ключ, автоинкремент)

    username (строка, уникальное значение)

    email (строка, уникальное значение)

    password (строка)
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    posts = relationship("Posts", back_populates="user")


class Posts(Base):
    """
    Таблица Posts должна содержать следующие поля:

    id (целое число, первичный ключ, автоинкремент)

    title (строка)

    content (текст)

    user_id (целое число, внешний ключ, ссылающийся на поле id таблицы Users)
    """

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("Users", back_populates="posts")


# Выберите одну из баз данных: MSSQL, __SQLite__, PostgreSQL, MySQL.
engine = create_engine("sqlite:///test.db")
Base.metadata.create_all(engine)
