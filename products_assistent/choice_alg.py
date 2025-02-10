import logging
from products_assistent.config_count import PRODUCT_COUNT

logger = logging.getLogger(__name__)


def get_some_first_products(products, products_count):
    return products[:products_count]


def get_leaderboard(products):
    best_products = get_some_first_products(products, PRODUCT_COUNT)

    return sorted(
        best_products,
        key=lambda prd: (
            prd.price,
            prd.avg_grade * prd.num_of_grades,
        ),
    )
