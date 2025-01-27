from pathlib import Path
import requests
import logging
from datetime import datetime

from products_assistent.products import get_products_list
from products_assistent.choice_alg import get_leaderboard
from products_assistent.show_data import show_data, show_product
from products_assistent.work_with_db import manage_to_init_db
from products_assistent.db import products_table
from products_assistent.db import requests_table


logger = logging.getLogger(__name__)
products_repo = products_table.ProductsRepo(
    Path("db") / "products_assistent.db"
)
requests_repo = requests_table.RequestsRepo(
    Path("db") / "products_assistent.db"
)


# sony wh-1000xm4
# logitech g435
# playstation 5
PRODUCT = "sony wh-1000xm4"
MARKET_NAME = "market.yandex.ru"


def main():
    logging.basicConfig(level=logging.DEBUG)

    had_connected, err_text = manage_to_init_db(
        products_repo,
        requests_repo,
    )
    if not had_connected:
        logger.error("Ошибка в базе данных:")
        logger.error(err_text)
        return

    product_and_date = requests_repo.get_product_and_date_by_req(PRODUCT)
    if product_and_date is not None:
        product = product_and_date[0]
        date = product_and_date[1]
        if datetime.today().day == date.day:
            logger.info("Сегодня это продукт уже искали:")
            show_product(product)
            return

    with requests.Session() as s:
        products = get_products_list(s, PRODUCT, MARKET_NAME)

    if products is None:
        return

    if len(products) == 0:
        logger.info("Нет сильно отличающихся вариантов")
        return

    best_products = get_leaderboard(products)

    show_data(products_repo, requests_repo, best_products[0], PRODUCT)


if __name__ == "__main__":
    main()
