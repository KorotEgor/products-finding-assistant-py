import requests
import logging
from datetime import datetime


from products_assistent.products import get_products_list
from products_assistent.choice_alg import get_leaderboard
from products_assistent import show_data
from products_assistent.db.work_with_db import (
    manage_to_save_to_db,
)

logger = logging.getLogger(__name__)

# sony wh-1000xm4
# # logitech g435
# # playstation 5
# PRODUCT = "sony wh-1000xm4"
MARKET_NAME = "market.yandex.ru"


def get_product_data(product_req, products_repo, requests_repo):
    logging.basicConfig(level=logging.DEBUG)

    dbproduct = products_repo.get_dbproduct_by_req(product_req)
    if dbproduct is not None:
        if datetime.today().day == dbproduct.date.day:
            logger.info("Сегодня это продукт уже искали:")
            diff_price, avg_price = products_repo.get_diff_avg_price_by_prd_id(
                dbproduct.id,
            )
            show_data.show_product(diff_price, avg_price, dbproduct)
            return dbproduct, diff_price, avg_price

    with requests.Session() as s:
        products = get_products_list(s, product_req, MARKET_NAME)

    if isinstance(products, Exception):
        return "Не корректный запрос", "", ""

    if products is None:
        logger.info("Нет похожих товаров в интернете")
        return "Нет похожих товаров в интернете", "", ""

    if len(products) == 0:
        logger.info("Нет сильно отличающихся вариантов")
        return "Нет сильно отличающихся вариантов", "", ""

    best_products = get_leaderboard(products)

    prd_id = manage_to_save_to_db(
        products_repo,
        requests_repo,
        best_products[0],
        product_req,
    )

    if prd_id is None:
        return "Не удалось найти товар", "", ""

    logger.info("Товар добавлен в базу данных: ")
    diff_price, avg_price = products_repo.get_diff_avg_price_by_prd_id(
        prd_id,
    )
    show_data.show_product(
        diff_price,
        avg_price,
        best_products[0],
    )
    return best_products[0], diff_price, avg_price
