from dataclasses import dataclass
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session,
    g,
)
from sqlite3 import DatabaseError
import logging
from werkzeug.security import check_password_hash

from products_assistent.app.utils import (
    check_username,
    check_email,
    check_password,
)
from products_assistent.db.conn_to_db import get_db
from products_assistent.db import users_table

logger = logging.getLogger(__name__)
bp = Blueprint("auth", __name__, url_prefix="/auth")


@dataclass
class FieldsFormErrs:
    username: list
    email: list
    password: list


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        users_repo = users_table.UsersRepo(get_db())

        user = users_repo.get_user_by_email(user_id)
        if isinstance(user, DatabaseError):
            logger.error(f"Ошибка при получении пользователя: {user}")
        else:
            g.user = lambda: user


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        fields_errs = FieldsFormErrs(
            username=check_username(username),
            email=check_email(email),
            password=check_password(password),
        )

        if fields_errs.username or fields_errs.email or fields_errs.password:
            flash("Не верно заполнены поля", "alert alert-warning")
            return render_template(
                "auth/register.html",
                fields_errs=fields_errs,
            )

        users_repo = users_table.UsersRepo(get_db())

        user = users_repo.get_user_by_email(email)
        if isinstance(user, DatabaseError):
            logger.error(f"Ошибка при получении пользователя: {user}")
            flash("Ошибка на стороне сервера", "alert alert-danger")
            return redirect(url_for("main.home"))
        elif user is not None:
            flash(
                f"Пользователь с такой почтой {email} уже создан",
                "alert alert-warning",
            )
            return redirect(url_for("auth.register"))

        err = users_repo.save_user(username, email, password)
        if err is None:
            flash("Пользователь успешно зарегистрирован", "alert alert-success")
            return redirect(url_for("main.home"))
        else:
            logger.error(err)
            flash(err, "alert alert-danger")

    return render_template(
        "auth/register.html",
        fields_errs=FieldsFormErrs(
            username=[],
            email=[],
            password=[],
        ),
    )


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        fields_errs = FieldsFormErrs(
            username=[],
            email=check_email(email),
            password=check_password(password),
        )

        if fields_errs.username or fields_errs.email or fields_errs.password:
            flash("Не верно заполнены поля", "alert alert-warning")
            return render_template(
                "auth/login.html",
                fields_errs=fields_errs,
            )

        users_repo = users_table.UsersRepo(get_db())

        user = users_repo.get_user_by_email(email)
        if isinstance(user, DatabaseError):
            logger.error(f"Ошибка при получении пользователя: {user}")
            flash("Ошибка на стороне сервера", "alert alert-danger")
            return redirect(url_for("main.home"))
        elif user is None:
            flash(
                f"Пользователя с почтой {email} не существует",
                "alert alert-warning",
            )
            return redirect(url_for("auth.login"))

        if not check_password_hash(user[3], password):
            flash(
                "Неверный пароль",
                "alert alert-warning",
            )
            return redirect(url_for("auth.login"))
        else:
            session.clear()
            session["user_id"] = user[0]
            flash("Успешный вход в систему", "alert alert-success")
            return redirect(url_for("main.home"))

    return render_template(
        "auth/login.html",
        fields_errs=FieldsFormErrs(
            username=[],
            email=[],
            password=[],
        ),
    )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.home"))
