from products_assistent.work_with_db import (
    manage_to_save_to_db,
    manage_to_update_db,
)
from products_assistent.utils import get_avg_and_diff_price


import logging

logger = logging.getLogger(__name__)


def show_product(avg_price, diff_price, product):
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
    logger.info(f"Средняя цена за все время: {avg_price}")
    logger.info(f"Изменение цены за все время: {diff_price}")


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


def show_data(products_repo, requests_repo, prd_prices_repo, product, request):
    repo_product = products_repo.get_product_by_name(product.name)

    if repo_product is None:
        flag, prd_id = manage_to_save_to_db(
            products_repo,
            requests_repo,
            prd_prices_repo,
            product,
            request,
        )
        if flag:
            logger.info("Товар добавлен в базу данных: ")

            avg_price, diff_price = get_avg_and_diff_price(
                prd_prices_repo,
                prd_id,
            )
            show_product(avg_price, diff_price, product)
            return
        else:
            logger.error("Не удалось сохранить товар")
            return

    product_id, _ = repo_product
    had_updated, err_text = manage_to_update_db(
        products_repo,
        requests_repo,
        prd_prices_repo,
        product_id,
        product,
        request,
    )
    if not had_updated:
        logger.error("Не удалось обновить товар")
        logger.error(err_text)
        return

    price_diff = product.price - repo_product.price
    avg_grades_diff = product.avg_grade - repo_product.avg_grade
    num_of_grades_diff = product.num_of_grades - repo_product.num_of_grades
    changes_text = get_changes_text(
        price_diff, avg_grades_diff, num_of_grades_diff
    )

    logger.info(changes_text)
    show_product(avg_price, diff_price, product)
