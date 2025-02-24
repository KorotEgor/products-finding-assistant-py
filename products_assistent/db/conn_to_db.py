import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    # получаем db из окружения flask
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )

    return g.db


#  закрываем подключение, если оно есть
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


# исполняем файл со схемой базы
def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


# скрипт подключение к db
@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    # для первого tells Flask to call that function when cleaning up after returning the response.
    # не очень понял надо ли
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# переформатирует все даты в "нормальный" формат
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)
