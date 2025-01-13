from dataclasses import dataclass

from products_assistent.products import Product


@dataclass
class ProductStats:
    product: Product
    name_match_rate: int
    mark: int


def get_avgs(products):
    products_count = len(products)
    prices_sum = 0
    grades_sum = 0
    mn_diff_prices = products[0].price * 2
    prev_product = products[0]

    for product in products:
        prices_sum += product.price
        grades_sum += product.gen_grade

        diff_prices = abs(prev_product.price - product.price)
        if diff_prices != 0:
            mn_diff_price = min(mn_diff_prices, diff_prices)
        prev_product = product

    avg_prices = prices_sum / products_count
    avg_grades = grades_sum / products_count
    return round(avg_prices), round(avg_grades), mn_diff_price


def get_name_rate(name, cor_name):
    counter = 0
    for word in name:
        if word in cor_name:
            counter += 1
    return counter


# также удаление с низкими оценками
def conv_to_stat(products, cor_name):
    avg_prices, avg_grades, mn_prices_diff = get_avgs(products)
    stats_products = []
    for product in products:
        # это удаление
        if product.gen_grade < avg_grades:
            continue

        mark = (product.price - avg_prices) // mn_prices_diff
        name_match_rate = get_name_rate(
            set(product.name.lower().split()),
            set(cor_name.lower().split()),
        )
        stats_products.append(
            ProductStats(product=product, name_match_rate=name_match_rate, mark=mark)
        )
    return stats_products


def get_leaderboard(products, cor_name):
    stats_products = conv_to_stat(products, cor_name)
    stats_products.sort(
        key=lambda prd: (
            -prd.name_match_rate,
            prd.mark,
            prd.product.gen_grade,
        ),
    )
    return [stats_product.product for stats_product in stats_products]
