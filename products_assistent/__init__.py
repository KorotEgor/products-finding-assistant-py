import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv()

# для тестов как параметр
# test_config=None
def create_app():
    # создаем окружение
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("DEV_KEY"),
        DATABASE=os.path.join(app.instance_path, 'products_assistent.sqlite'),
    )

    # для тестов
    # if test_config is not None:
    #     app.config.from_mapping(test_config)

    # проверка есть ли окружение
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from products_assistent.db import conn_to_db
    conn_to_db.init_app(app)

    return app
