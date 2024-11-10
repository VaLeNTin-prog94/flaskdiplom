# для настройки баз данных
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base

# для создания отношений между таблицами
from sqlalchemy.orm import relationship

# для настроек
from sqlalchemy import create_engine

# создание экземпляра declarative_base
Base = declarative_base()

from datetime import datetime

# создает экземпляр create_engine в конце файла
engine = create_engine('sqlite:///diplom.db')
Base.metadata.create_all(engine)


class User(Base):
    """
    Класс в котором описываются поля Пользователя в базе данных
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)

    def __str__(self):
        """
                Cпециальный метод, предназначенный для представления строкового представления объекта
                :return:Возвращает удобочитаемое (или неформальное) строковое представление объекта.
                """
        return self.username


class Category(Base):
    """
    Класс в котором описываются поля Категорий в базе данных
    Наследуется от базового класса
    """
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        """
        Cпециальный метод, предназначенный для представления строкового представления объекта
        :return:Возвращает удобочитаемое (или неформальное) строковое представление объекта.
        """
        return self.name


class Bakes(Base):
    """
        Класс в котором описываются поля Выпечек в базе данных
        """
    __tablename__ = 'bakes'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    text = Column(String(1000), nullable=False)
    time = Column(DateTime, default=datetime.utcnow)
    cat_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship(Category)


engine = create_engine('sqlite:///diplom.db')

# Добавляем поля в базу данных
Base.metadata.create_all(engine)
