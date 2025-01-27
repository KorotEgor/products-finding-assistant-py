from products_assistent.work_with_db import manage_to_save_product, manage_to_update_product


import logging

logger = logging.getLogger(__name__)


def show_product(product):
    logger.info("Название:")
    logger.info(product.name)
    logger.info("URL адрес:")
    logger.info(product.url)
    logger.info("Цена:")
    logger.info(product.price)
    logger.info("Количество оценок:")
    logger.info(product.avg_grade)
    logger.info("Средняя оценка:")
    logger.info(product.num_of_grades)


def get_changes_text(price_diff, avg_grades_diff, num_of_grades_diff):
    changes_text = ["ась"]
    c = 0
    if price_diff < 0:
        price_diff = abs(price_diff)
        changes_text.append(f"цена уменьшилась на {price_diff}")
    elif price_diff > 0:
        changes_text.append(f"цена увеличилась на {price_diff}")
    else:
        c += 1

    if avg_grades_diff > 0:
        changes_text[0] = "ись"

        if len(changes_text) > 1:
            changes_text.append("и")

        text = f"количество оценок увеличилось на {num_of_grades_diff}, а средняя оценка"
        if avg_grades_diff > 0:
            text += "увеличелась на " + avg_grades_diff
        else:
            text += "уменьшилась на " + avg_grades_diff

        changes_text.append(text)
    else:
        c += 1

    if c < 2:
        return "Товар был обнавлен" + " ".join(changes_text)
    else:
        return "Товар был взят из базы данных."


def show_data(product, products_repo):
    repo_product = products_repo.get_product_by_name(product.name)

    if repo_product is None:
        if manage_to_save_product(products_repo, product):
            logger.info("Товар добавлен в базу данных: ")
            show_product(product)
            return
        else:
            logger.error("Не удалось сохранить товар")

    if not manage_to_update_product(products_repo, product):
        logger.error("Не удалось обновить товар")
        return

    price_diff = product.price - repo_product.price
    avg_grades_diff = product.avg_grade - repo_product.avg_grade
    num_of_grades_diff = product.num_of_grades - repo_product.num_of_grades
    changes_text = get_changes_text(
        price_diff, avg_grades_diff, num_of_grades_diff
    )

    logger.info(changes_text)
    show_product(product)
