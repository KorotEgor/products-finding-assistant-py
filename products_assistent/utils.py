def get_avg_and_diff_price(prd_prices_repo, prd_id):
    min_price, max_price, avg_price = (
        prd_prices_repo.get_min_max_avg_price_by_prd_id(prd_id)
    )
    return avg_price, max_price - min_price
