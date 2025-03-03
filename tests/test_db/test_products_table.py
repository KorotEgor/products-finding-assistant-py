import pytest
from sqlite3 import DatabaseError

from products_assistent import products
from products_assistent.db import products_table
from products_assistent.db.conn_to_db import get_db


@pytest.fixture
def get_product(app):
    test_product = products.Product(
        name="test_product",
        url="test_url",
        price=1,
        avg_grade=2.0,
        num_of_grades=3,
    )
    return test_product


def test_save_product(app, get_product):
    with app.app_context():
        db = get_db()
        prds_repo = products_table.ProductsRepo(db)

        test_product = get_product

        err_text = "не верно вернул id запроса"
        assert prds_repo.save_product(1, test_product) == 2, err_text

        err_text = "не сохранил запрос"
        assert db.execute(
            "SELECT COUNT(*) FROM products",
        ).fetchone() == (2,), err_text

        err_text = "не выкинул DatabaseError"
        assert isinstance(prds_repo.save_product(None, test_product), DatabaseError)
