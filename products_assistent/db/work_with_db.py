from sqlite3 import DatabaseError


def manage_to_init_db(products_repo, reqs_repo):
    try:
        reqs_repo.create_table_requests()
        products_repo.create_table_products()
    except (DatabaseError, AttributeError) as e:
        return e

    return None


def manage_to_save_to_db(products_repo, reqs_repo, product, req):
    try:
        req_id = reqs_repo.save_request(req)
        prd_id = products_repo.save_product(req_id, product)
    except (DatabaseError, AttributeError):
        return None

    return prd_id
