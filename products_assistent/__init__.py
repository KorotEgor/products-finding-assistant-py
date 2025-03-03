import os
import logging
from flask import Flask
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


def create_app(test_config=None):
    # создаем окружение
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("DEV_KEY"),
        DATABASE=os.path.join(app.instance_path, "products_assistent.sqlite"),
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    # проверка есть ли окружение
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from products_assistent.db import conn_to_db

    conn_to_db.init_app(app)

    from products_assistent.app import bp

    app.register_blueprint(bp)

    return app
