from pathlib import Path
import requests
import logging
from datetime import datetime

from products_assistent.products import get_products_list
from products_assistent.choice_alg import get_leaderboard
from products_assistent import show_data
from products_assistent.db.work_with_db import (
    manage_to_init_db,
    manage_to_save_to_db,
)
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

    err_text = manage_to_init_db(
        products_repo,
        requests_repo,
    )
    if err_text is not None:
        logger.error("Ошибка в базе данных:")
        logger.error(err_text)
        return

    dbproduct = products_repo.get_dbproduct_by_req(PRODUCT)
    if dbproduct is not None:
        if datetime.today().day == dbproduct.date.day:
            logger.info("Сегодня это продукт уже искали:")
            diff_price, avg_price = products_repo.get_diff_avg_price_by_prd_id(
                dbproduct.id,
            )
            show_data.show_product(diff_price, avg_price, dbproduct)
            return

    with requests.Session() as s:
        products = get_products_list(s, PRODUCT, MARKET_NAME)

    if products is None:
        return

    if len(products) == 0:
        logger.info("Нет сильно отличающихся вариантов")
        return

    best_products = get_leaderboard(products)

    prd_id = manage_to_save_to_db(
        products_repo,
        requests_repo,
        best_products[0],
        PRODUCT,
    )

    if prd_id is not None:
        logger.info("Товар добавлен в базу данных: ")
        diff_price, avg_price = products_repo.get_diff_avg_price_by_prd_id(
            prd_id,
        )
        show_data.show_product(
            diff_price,
            avg_price,
            best_products[0],
        )
    else:
        logger.error("Не удалось сохранить товар")


if __name__ == "__main__":
    main()
