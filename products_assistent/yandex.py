import requests
import logging
from datetime import datetime

from products_assistent.config import PRODUCT_COUNT
from products_assistent.products import get_products_list
from products_assistent.choice_alg import get_leaderboard
from products_assistent import show_data
from products_assistent.db.work_with_db import (
    manage_to_save_to_db,
)

logger = logging.getLogger(__name__)

# sony wh-1000xm4
# logitech g435
# playstation 5
# PRODUCT = "sony wh-1000xm4"
MARKET_NAME = "market.yandex.ru"


def is_today(dbproduct):
    if dbproduct is None:
        return False

    return datetime.today().day == dbproduct.date.day


def get_product_data(product_req, products_repo, requests_repo):
    logging.basicConfig(level=logging.DEBUG)

    dbproduct = products_repo.get_dbproduct_by_req(product_req)
    if is_today(dbproduct):
        logger.info("Сегодня это продукт уже искали:")
        diff_price, avg_price = products_repo.get_diff_avg_price_by_prd_id(
            product_req,
        )
        show_data.show_product(diff_price, avg_price, dbproduct)
        return (
            "Продукт удачно найден",
            "alert alert-success",
            dbproduct,
            diff_price,
            avg_price,
        )

    with requests.Session() as s:
        products = get_products_list(s, product_req, MARKET_NAME)

    if isinstance(products, Exception):
        return "Не корректный запрос", "alert alert-danger", "", "", ""

    if products is None or len(products) == 0:
        logger.info("Нет похожих товаров в интернете")
        return (
            "Нет похожих товаров в интернете",
            "alert alert-danger",
            "",
            "",
            "",
        )

    best_products = get_leaderboard(products, PRODUCT_COUNT)

    prd_id = manage_to_save_to_db(
        products_repo,
        requests_repo,
        best_products[0],
        product_req,
    )

    if prd_id is None:
        return "Не удалось найти товар", "alert alert-danger", "", "", ""

    logger.info("Товар добавлен в базу данных: ")
    diff_price, avg_price = products_repo.get_diff_avg_price_by_prd_id(
        product_req,
    )
    show_data.show_product(
        diff_price,
        avg_price,
        best_products[0],
    )
    return (
        "Продукт удачно найден",
        "alert alert-success",
        best_products[0],
        diff_price,
        avg_price,
    )
