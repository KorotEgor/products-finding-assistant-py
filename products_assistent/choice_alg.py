from dataclasses import dataclass
import re
import logging

from products_assistent.products import Product

logger = logging.getLogger(__name__)
prog = re.compile(r"[^\w\s]")


@dataclass
class ProductStats:
    product: Product
    name_match_rate: int


def get_name_rate(name, cor_name):
    counter = 0
    for word in name:
        new_word = word[:-1] + prog.sub("", word[-1])
        if new_word in cor_name:
            counter += 1
    return counter


def conv_to_stat(products, cor_name):
    stats_products = []
    for product in products:
        name_match_rate = get_name_rate(
            set(product.name.lower().split()),
            set(cor_name.lower().split()),
        )
        stats_products.append(
            ProductStats(product=product, name_match_rate=name_match_rate)
        )
    return stats_products


def get_rait_leaderboard_of_10(products, n):
    return sorted(
        products,
        reverse=True,
        key=lambda prd: prd.num_of_grades * prd.avg_grade,
    )[:n]


def get_leaderboard(products, cor_name):
    rait_leaderboard_of_10 = get_rait_leaderboard_of_10(products, 10)

    stats_products = conv_to_stat(rait_leaderboard_of_10, cor_name)

    stats_products.sort(
        key=lambda prd: (-prd.name_match_rate, prd.product.price),
    )

    logger.debug(
        [stats_product.name_match_rate for stats_product in stats_products]
    )
    return [stats_product.product for stats_product in stats_products]
