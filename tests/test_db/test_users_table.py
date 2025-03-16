from products_assistent.db import users_table
from products_assistent.db.conn_to_db import get_db


def test_save_user(app):
    with app.app_context():
        db = get_db()
        reqs_repo = users_table.UsersRepo(db)

        assert (
            reqs_repo.save_user("test", "test_email@gmail.com", "Test_pass123!")
            == "Ошибка при сохранении пользователя: UNIQUE constraint failed: users.email"
        )

        assert (
            reqs_repo.save_user(
                "test", "test_email@gmail.right", "Test_pass123!"
            )
            is None
        )


def test_get_user_by_email(app):
    with app.app_context():
        db = get_db()
        reqs_repo = users_table.UsersRepo(db)

        assert reqs_repo.get_user_by_email("Empty") is None

        assert reqs_repo.get_user_by_email("test_email@gmail.com")[:-2] == (
            1,
            "test_name",
            "test_email@gmail.com",
            "Test_pass123!",
        )


def test_get_user_by_id(app):
    with app.app_context():
        db = get_db()
        reqs_repo = users_table.UsersRepo(db)

        assert reqs_repo.get_user_by_id(2) is None

        assert reqs_repo.get_user_by_id(1)[:-2] == (
            1,
            "test_name",
            "test_email@gmail.com",
            "Test_pass123!",
        )
