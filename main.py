"""
Часть 3: Базовые операции с базой данных в веб-приложении

Создайте простое веб-приложение на FastAPI.

Интегрируйте SQLAlchemy в ваше веб-приложение.

Реализация CRUD-операций:

Реализуйте веб-страницы для выполнения CRUD-операций (создание, чтение, обновление, удаление) с
записями в таблицах Users и Posts.

Страницы должны включать:

Форму для создания нового пользователя/поста.

Список всех пользователей/постов с возможностью редактирования и удаления.

Страницу для редактирования информации о пользователе/посте.
"""

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from create_tables import Users, Posts

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


class UserPublic(BaseModel):
    """
    Модель пользователя без поля password
    """

    id: int
    username: str
    email: str


class UserCreate(BaseModel):
    """
    Форма создания пользователя
    """

    username: str
    email: str
    password: str


class PostCreate(BaseModel):
    """
    Форма создания поста
    """

    title: str
    content: str
    user_id: int


def get_db():
    """
    Возвращает объект для доступа к БД
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Создаёт пользователя
    """
    new_user = Users(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    """
    Перечисляет пользователей
    """
    return [UserPublic(**user.__dict__) for user in (db.query(Users).all())]


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Возвращает информацию о пользователе
    """
    return UserPublic(**db.query(Users).filter(Users.id == user_id).first().__dict__)


@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    """
    Обновляет информацию о пользователе
    """
    db_user = db.query(Users).filter(Users.id == user_id).first()
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Удаляет пользователя
    """
    db_user = db.query(Users).filter(Users.id == user_id).first()
    db.query(Posts).filter(Posts.user_id == db_user.id).delete()
    db.delete(db_user)
    db.commit()
    return {"message": "Пользователь и все его посты удалены"}


@app.post("/posts/")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """
    Создаёт пост
    """
    new_post = Posts(title=post.title, content=post.content, user_id=post.user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/")
def list_posts(db: Session = Depends(get_db)):
    """
    Возвращает список постов
    """
    return db.query(Posts).all()


@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Возвращает пост
    """
    return db.query(Posts).filter(Posts.id == post_id).first()


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    """
    Обновляет пост
    """
    db_post = db.query(Posts).filter(Posts.id == post_id).first()
    db_post.title = post.title
    db_post.content = post.content
    db_post.user_id = post.user_id
    db.commit()
    db.refresh(db_post)
    return db_post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Удаляет пост
    """
    db_post = db.query(Posts).filter(Posts.id == post_id).first()
    db.delete(db_post)
    db.commit()
    return {"message": "Пост удалён"}
