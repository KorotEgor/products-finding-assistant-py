# import pytest
from sqlite3 import DatabaseError

from products_assistent.yandex import products
from products_assistent.db import products_table
from products_assistent.db.conn_to_db import get_db


def test_save_product(app):
    with app.app_context():
        db = get_db()
        prds_repo = products_table.ProductsRepo(db)

        test_product = products.Product(
            name="test_product",
            url="test_url",
            price=1,
            avg_grade=2.0,
            num_of_grades=3,
        )

        err_text = "не верно вернул id запроса"
        assert prds_repo.save_product(1, test_product) == 4, err_text

        err_text = "не сохранил запрос"
        assert db.execute(
            "SELECT COUNT(*) FROM products",
        ).fetchone() == (4,), err_text

        err_text = "не выкинул DatabaseError"
        assert isinstance(
            prds_repo.save_product(None, test_product), DatabaseError
        )


def test_get_dbproduct_by_req(app):
    with app.app_context():
        db = get_db()
        prds_repo = products_table.ProductsRepo(db)

        dbproduct = prds_repo.get_dbproduct_by_req("test_req1")

        err_text = "не верный тип возвращаемых данных"
        assert isinstance(dbproduct, products_table.DBProduct), err_text

        err_text = "не верный продукт получен из бд"
        assert dbproduct.id == 1, err_text

        err_text = "возвращает не None при запросе несуществующего продукта"
        assert prds_repo.get_dbproduct_by_req("None_req") is None, err_text

        # не знаю как спровоцировать такое поведение
        # with pytest.raises(DatabaseError):
        #     prds_repo.get_dbproduct_by_req(None)


def test_get_diff_avg_price_by_prd_id(app):
    with app.app_context():
        db = get_db()
        prds_repo = products_table.ProductsRepo(db)

        err_text = "не верно вернул результат функции"
        assert prds_repo.get_diff_avg_price_by_prd_id("test_req1") == (
            1,
            1.5,
        ), err_text

        err_text = "возвращает не None при запросе несуществующего продукта"
        assert prds_repo.get_diff_avg_price_by_prd_id("None_req") is None, err_text

        # не знаю как спровоцировать такое поведение
        # with pytest.raises(DatabaseError):
        #     prds_repo.get_diff_avg_price_by_prd_id(None)
