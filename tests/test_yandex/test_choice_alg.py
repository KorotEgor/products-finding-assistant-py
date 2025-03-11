import pytest
import random

from products_assistent.yandex.choice_alg import get_leaderboard
from products_assistent.yandex.products import Product

_TEST_PRD_COUNT = 4


@pytest.fixture
def get_products():
    products = [
        Product("c", "d", 0, 2.0, 1),
        Product("aaa", "bbb", 1, 2.0, 1),
        Product("a", "b", 1, 1.0, 1),
        Product("aa", "bb", 1, 1.0, 1),
        Product("cc", "dd", 2, 1.0, 0),
    ]
    cor_products = products[:_TEST_PRD_COUNT]
    random.shuffle(products)
    return products, cor_products


def test_get_leaderboard(get_products):
    products, cor_products = get_products

    testing_products = get_leaderboard(products, _TEST_PRD_COUNT)
    assert len(testing_products) == _TEST_PRD_COUNT, "неверное кол-во продуктов"
    assert cor_products == testing_products, "неверная сортирока продуктов"
