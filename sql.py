from sqlalchemy import create_engine, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(50))

    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(String(500))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r})"

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

def run_crud_operations():
    with SessionLocal() as session:
        print("--- [C]reate / Создание ---")
        new_user = User(
            username="alex_purple", 
            email="alex@purpleschool.ru",
            posts=[
                Post(title="Изучаем SQLAlchemy", content="ORM — это удобно!"),
                Post(title="Второй пост", content="Продолжаем кодить на Python.")
            ]
        )
        session.add(new_user)
        session.commit()  
        print(f"Пользователь сохранен с ID: {new_user.id}")

    with SessionLocal() as session:
        print("\n--- [R]ead / Чтение ---")
        user = session.query(User).filter_by(username="alex_purple").first()
        print(f"Найден пользователь: {user} (Email: {user.email})")
        print(f"Его публикации: {user.posts}")

    with SessionLocal() as session:
        print("\n--- [U]pdate / Обновление ---")
        user = session.query(User).filter_by(username="alex_purple").first()
        if user:
            user.email = "new_alex@purpleschool.ru"  
            session.commit()
            print("Email успешно обновлен.")

    with SessionLocal() as session:
        user = session.query(User).filter_by(username="alex_purple").first()
        print(f"Обновленный email в БД: {user.email}")

    with SessionLocal() as session:
        print("\n--- [D]elete / Удаление ---")
        user = session.query(User).filter_by(username="alex_purple").first()
        if user:
            session.delete(user)  
            session.commit()
            print("Пользователь и его посты удалены.")

    with SessionLocal() as session:
        users_count = session.query(User).count()
        posts_count = session.query(Post).count()
        print(f"Осталось пользователей в БД: {users_count}, постов: {posts_count}")


if __name__ == "__main__":
    run_crud_operations()
