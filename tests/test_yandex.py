import datetime

from products_assistent.yandex import is_today
from products_assistent.db.products_table import DBProduct


def test_is_today():
    today_product = DBProduct(
        1,
        "test_name",
        "test_url",
        1,
        1.0,
        3,
        datetime.datetime.today(),
    )

    yesterday_product = DBProduct(
        1,
        "test_name",
        "test_url",
        1,
        1.0,
        3,
        today_product.date - datetime.timedelta(days=1),
    )

    tomorrow_product = DBProduct(
        1,
        "test_name",
        "test_url",
        1,
        1.0,
        3,
        today_product.date + datetime.timedelta(days=1),
    )

    err_text = "не верно определил сегодня ли этот продукт"
    assert is_today(today_product) is True, err_text
    assert is_today(yesterday_product) is False, err_text
    assert is_today(tomorrow_product) is False, err_text
