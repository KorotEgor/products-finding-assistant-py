from dataclasses import dataclass
from datetime import datetime
from sqlite3 import DatabaseError
from werkzeug.security import generate_password_hash


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    photo: str
    created_at: datetime
    updated_at: datetime


class UsersRepo:
    def __init__(self, db):
        self.db = db

    def save_user(self, name, email, password):
        try:
            self.db.execute(
                """
                    INSERT INTO users (name, email, password)
                    VALUES (?, ?, ?)
                """,
                (
                    name,
                    email,
                    generate_password_hash(password),
                ),
            )
            self.db.commit()
        except DatabaseError as err:
            return f"Ошибка при сохранении пользователя: {err}"

        return None

    def get_user_by_email(self, email):
        try:
            cur = self.db.execute(
                """
                    SELECT *
                    FROM users
                    WHERE email = ?
                """,
                (email,),
            )
            user = cur.fetchone()
            if user is None:
                return None

        except DatabaseError as err:
            return err

        return User(*user)

    def get_user_by_id(self, id):
        try:
            cur = self.db.execute(
                """
                    SELECT *
                    FROM users
                    WHERE id = ?
                """,
                (id,),
            )
            user = cur.fetchone()
            if user is None:
                return None

        except DatabaseError as err:
            return err

        return User(*user)
