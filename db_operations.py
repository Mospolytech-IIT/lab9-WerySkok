"""
Часть 2: Взаимодействие с базой данных
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from create_tables import Users, Posts

engine = create_engine("sqlite:///test.db")
Session = sessionmaker(bind=engine)
session = Session()

# Напишите программу, которая добавляет в таблицу Users несколько записей с разными значениями полей
# username, email и password.
user1 = Users(username="alex", email="alex@example.com", password="pass1")
user2 = Users(username="maria", email="maria@example.com", password="pass2")
session.add_all([user1, user2])
session.commit()

# Напишите программу, которая добавляет в таблицу Posts несколько записей, связанных с
# пользователями из таблицы Users.
post1 = Posts(title="Первый пост", content="Контент поста 1", user_id=user1.id)
post2 = Posts(title="Второй пост", content="Контент поста 2", user_id=user1.id)
post3 = Posts(title="Третий пост", content="Контент поста 3", user_id=user2.id)
session.add_all([post1, post2, post3])
session.commit()

# Напишите программу, которая извлекает все записи из таблицы Users.
all_users = session.query(Users).all()
for user in all_users:
    print(user.id, user.username, user.email)

# Напишите программу, которая извлекает все записи из таблицы Posts, включая информацию о
# пользователях, которые их создали.
all_posts = session.query(Posts).options(joinedload(Posts.user)).all()
for post in all_posts:
    print(post.id, post.title, post.content, post.user_id)

# Напишите программу, которая извлекает записи из таблицы Posts, созданные конкретным пользователем.
posts_by_alex = session.query(Posts).join(Users).filter(Users.username == "alex").all()
for post in posts_by_alex:
    print(post.title, "принадлежит alex")

# Напишите программу, которая обновляет поле email у одного из пользователей.
alex = session.query(Users).filter_by(username="alex").first()
alex.email = "new_alex@example.com"
session.commit()

# Напишите программу, которая обновляет поле content у одного из постов.
post_for_update = session.query(Posts).filter_by(title="Первый пост").first()
post_for_update.content = "Обновлённый контент"
session.commit()

# Напишите программу, которая удаляет один из постов.
post_to_delete = session.query(Posts).filter_by(title="Второй пост").first()
session.delete(post_to_delete)
session.commit()

# Напишите программу, которая удаляет пользователя и все его посты.
maria = session.query(Users).filter_by(username="maria").first()
session.query(Posts).filter(Posts.user_id == maria.id).delete()
session.delete(maria)
session.commit()
