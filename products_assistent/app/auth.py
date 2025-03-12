from flask import (
    Blueprint,
    flash,
    # g,
    redirect,
    render_template,
    request,
    # session,
    url_for,
)
from sqlite3 import DatabaseError
import logging

from products_assistent.db.conn_to_db import get_db
from products_assistent.db import users_table

logger = logging.getLogger(__name__)
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        errors = []

        if not username:
            errors += ["Имя - обязательное поле"]
        elif not email:
            errors += ["Почта - обязательное поле"]
        elif not password:
            errors += ["Пароль - обязательное поле"]

        if errors:
            flash(*errors, "alert alert-warning")
            return redirect(url_for("auth.register"))

        users_repo = users_table.UsersRepo(get_db())

        err = users_repo.get_user_by_email(email)
        if isinstance(err, DatabaseError):
            logger.error(err)
            flash("Ошибка на стороне сервера", "alert alert-danger")
            return redirect(url_for("main.home"))
        elif err is not None:
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

    return render_template("auth/register.html")
