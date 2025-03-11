import os
from pathlib import Path
import tempfile

import pytest
from products_assistent import create_app
from products_assistent.db.conn_to_db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


# создает временный файл базы данных
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        "SECRET_KEY": "test_key",
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # Path
    os.close(db_fd)
    os.unlink(db_path)


# эмитация клиента без сервера
@pytest.fixture
def client(app):
    return app.test_client()


# может вызвать Click команды, созданные в __init__.py в products_assistent
@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class RequestActions(object):
    def __init__(self, client):
        self.client = client

    def post_req(self, product_req="test_user_req"):
        return self._client.post(
            '/',
            data={"product_req": product_req},
        )


@pytest.fixture
def req(client):
    return RequestActions(client)
