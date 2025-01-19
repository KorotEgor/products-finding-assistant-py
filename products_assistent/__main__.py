import requests
from products_assistent.products import get_products_list
from products_assistent.choice_alg import get_leaderboard
import logging

logger = logging.getLogger(__name__)

# sony wh-1000xm4
# logitech g435
# playstation 5
PRODUCT = "sony wh-1000xm4"
MARKET_NAME = "market.yandex.ru"


def show_data(products):
    for product in products:
        logger.info(product)


def main():
    logging.basicConfig(level=logging.DEBUG)
    with requests.Session() as s:
        products = get_products_list(s, PRODUCT, MARKET_NAME)

    if products is None:
        return

    if len(products) == 0:
        logger.info("Нет сильно отличающихся вариантов")
        return

    best_products = get_leaderboard(products, PRODUCT)

    show_data(best_products)


if __name__ == "__main__":
    main()
