from pathlib import Path
import requests
import logging

from products_assistent.products import get_products_list
from products_assistent.choice_alg import get_leaderboard
from products_assistent.show_data import show_data
from products_assistent.work_with_db import manage_to_connect_to_db
from products_assistent.db import products_table
from products_assistent.db import requests_table


logger = logging.getLogger(__name__)
products_repo = products_table.ProductsRepo(Path("db") / "products_assistent.db")
requests_repo = requests_table.RequestsRepo(Path("db") / "products_assistent.db")


# sony wh-1000xm4
# logitech g435
# playstation 5
PRODUCT = "sony wh-1000xm4"
MARKET_NAME = "market.yandex.ru"


def main():
    logging.basicConfig(level=logging.DEBUG)

    had_connected, err_text = manage_to_connect_to_db(products_repo)
    if had_connected:
        logger.error("Ошибка в базе данных", err_text)
        return

    with requests.Session() as s:
        products = get_products_list(s, PRODUCT, MARKET_NAME)

    if products is None:
        return

    if len(products) == 0:
        logger.info("Нет сильно отличающихся вариантов")
        return

    best_products = get_leaderboard(products)

    show_data(best_products[0], products_repo)


if __name__ == "__main__":
    main()
