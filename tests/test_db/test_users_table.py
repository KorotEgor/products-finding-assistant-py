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

        user = reqs_repo.get_user_by_email("test_email@gmail.com")
        assert (user.id, user.name, user.email, user.password, user.photo) == (
            1,
            "test_name",
            "test_email@gmail.com",
            "Test_pass123!",
            "https://thumbs.dreamstime.com/b/%D0%BF%D1%80%D0%BE%D1%84%D0%B8%D0%BB%D1%8C-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F-%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%B0-%D0%BF%D1%80%D0%BE%D1%84%D0%B8%D0%BB%D1%8F-%D0%B0%D0%B2%D0%B0%D1%82%D0%B0%D1%80%D1%8B-%D0%BF%D0%BE-%D1%83%D0%BC%D0%BE%D0%BB%D1%87%D0%B0%D0%BD%D0%B8%D1%8E-179376714.jpg",
        )


def test_get_user_by_id(app):
    with app.app_context():
        db = get_db()
        reqs_repo = users_table.UsersRepo(db)

        assert reqs_repo.get_user_by_id(2) is None

        user = reqs_repo.get_user_by_id(1)
        assert (user.id, user.name, user.email, user.password, user.photo) == (
            1,
            "test_name",
            "test_email@gmail.com",
            "Test_pass123!",
            "https://thumbs.dreamstime.com/b/%D0%BF%D1%80%D0%BE%D1%84%D0%B8%D0%BB%D1%8C-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F-%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%B0-%D0%BF%D1%80%D0%BE%D1%84%D0%B8%D0%BB%D1%8F-%D0%B0%D0%B2%D0%B0%D1%82%D0%B0%D1%80%D1%8B-%D0%BF%D0%BE-%D1%83%D0%BC%D0%BE%D0%BB%D1%87%D0%B0%D0%BD%D0%B8%D1%8E-179376714.jpg",
        )
