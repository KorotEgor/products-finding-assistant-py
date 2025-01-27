from sqlite3 import DatabaseError


def manage_to_connect_to_db(products_repo):
    try:
        products_repo.create_table_products()
    except (DatabaseError, AttributeError) as e:
        return False, e

    return True, ''


def manage_to_save_product(products_repo, product):
    try:
        products_repo.save_product(product)
    except (DatabaseError, AttributeError):
        return False

    return True


def manage_to_update_product(products_repo, product):
    try:
        products_repo.update_product(
            product.name,
            product.price,
            product.avg_grade,
            product.num_of_grades,
        )
    except (DatabaseError, AttributeError):
        return False

    return True
