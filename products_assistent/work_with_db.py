from sqlite3 import DatabaseError


def manage_to_init_db(products_repo, requests_repo, prd_prices_repo):
    try:
        products_repo.create_table_products()
        requests_repo.create_table_requests()
        prd_prices_repo.create_table_prd_prices()
    except (DatabaseError, AttributeError) as e:
        return False, e

    return True, ""


def manage_to_save_to_db(
    products_repo, requests_repo, prd_prices_repo, product, request
):
    try:
        product_id = products_repo.save_product(product)
        requests_repo.save_request(request, product_id)
        prd_prices_repo.save_prd_price(product_id, product.price)
    except (DatabaseError, AttributeError):
        return False, -1

    return True, product_id


def manage_to_update_db(
    products_repo, requests_repo, prd_prices_repo, prd_id, prd, req
):
    try:
        products_repo.update_product(
            prd.name,
            prd.price,
            prd.avg_grade,
            prd.num_of_grades,
        )
        requests_repo.update_request(req)
        prd_prices_repo.save_prd_price(prd_id)
    except (DatabaseError, AttributeError) as e:
        return False, e

    return True, ""
