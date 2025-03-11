def get_sorted_products(products):
    return sorted(
        products,
        key=lambda prd: (
            prd.price,
            -(prd.avg_grade * prd.num_of_grades),
            prd.name,
        ),
    )


def get_leaderboard(products, product_count):
    sorted_products = get_sorted_products(products)

    return sorted_products[:product_count]
