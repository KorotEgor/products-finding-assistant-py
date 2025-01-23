import requests
import logging
from sqlite3 import DatabaseError

from products_assistent.products import get_products_list
from products_assistent.choice_alg import get_leaderboard
from products_assistent.DB import products_table
from products_assistent import products


logger = logging.getLogger(__name__)
repo = products_table.ProductsTable()

# sony wh-1000xm4
# logitech g435
# playstation 5
PRODUCT = "sony wh-1000xm4"
MARKET_NAME = "market.yandex.ru"


# sqllite (добавить дату)
# выводить одно из этих сообщений: товар добавле в базу или цена/оценка были изменены или товар взят из базы
def show_product(product):
    logger.info('Название:')
    logger.info(product.name)
    logger.info('URL адрес:')
    logger.info(product.url)
    logger.info('Цена:')
    logger.info(product.price)
    logger.info('Количество оценок:')
    logger.info(product.avg_grade)
    logger.info('Средняя оценка:')
    logger.info(product.num_of_grades)


def get_changes_text(price_diff, avg_grades_diff, num_of_grades_diff):
    changes_text = ['ась']
    c = 0
    if price_diff < 0:
        price_diff = abs(price_diff)
        changes_text.append(f'цена уменьшилась на {price_diff}')
    elif price_diff > 0:
        changes_text.append(f'цена увеличилась на {price_diff}')
    else:
        c += 1

    if avg_grades_diff > 0:
        changes_text[0] = 'ись'

        if len(changes_text) > 1:
            changes_text.append('и')

        text = f'количество оценок увеличилось на {num_of_grades_diff}, а средняя оценка'
        if avg_grades_diff > 0:
            text += 'увеличелась на ' + avg_grades_diff
        else:
            text += 'уменьшилась на ' + avg_grades_diff

        changes_text.append(text)
    else:
        c += 1

    if c < 2:
        return 'Товар был обнавлен' + ' '.join(changes_text)
    else:
        return 'Товар был взят из базы данных.'


def show_data(product):
    repo_tuple_product = repo.get_product_by_name(product.name)

    if repo_tuple_product is None:
        try:
            repo.save_product(product)
        except (DatabaseError, AttributeError):
            logger.error('Не удалось сохранить товар')
            return

        logger.info('Товар добавлен в базу данных: ')
        show_product(product)
        return

    repo_product = products.Product(*repo_tuple_product)

    try:
        repo.update_product(
            product.name,
            product.price,
            product.avg_grade,
            product.num_of_grades,
        )
    except (DatabaseError, AttributeError):
        logger.error('Не удалось обновить товар')
        return

    price_diff = product.price - repo_product.price
    avg_grades_diff = product.avg_grade - repo_product.avg_grade
    num_of_grades_diff = product.num_of_grades - repo_product.num_of_grades
    changes_text = get_changes_text(price_diff, avg_grades_diff, num_of_grades_diff)

    logger.info(changes_text)


def main():
    logging.basicConfig(level=logging.DEBUG)

    try:
        repo.create_table_products()
    except (DatabaseError, AttributeError) as e:
        logger.error("Ошибка в базе данных: ", e)

    with requests.Session() as s:
        products = get_products_list(s, PRODUCT, MARKET_NAME)

    if products is None:
        return

    if len(products) == 0:
        logger.info("Нет сильно отличающихся вариантов")
        return

    best_products = get_leaderboard(products)

    show_data(best_products[0])


if __name__ == "__main__":
    main()
