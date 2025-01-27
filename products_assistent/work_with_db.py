from sqlite3 import DatabaseError


def manage_to_init_db(products_repo, requests_repo):
    try:
        products_repo.create_table_products()
        requests_repo.create_table_requests()
    except (DatabaseError, AttributeError) as e:
        return False, e

    return True, ""


def manage_to_save_to_db(products_repo, requests_repo, product, request):
    try:
        product_id = products_repo.save_product(product)
        requests_repo.save_request(request, product_id)
    except (DatabaseError, AttributeError):
        return False

    return True


def manage_to_update_db(products_repo, requests_repo, product, request):
    try:
        products_repo.update_product(
            product.name,
            product.price,
            product.avg_grade,
            product.num_of_grades,
        )
        requests_repo.update_request(request)
    except (DatabaseError, AttributeError) as e:
        return False, e

    return True, ""
