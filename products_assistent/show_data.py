import logging

logger = logging.getLogger(__name__)


def show_product(diff_price, avg_price, product):
    logger.info(f"Название: {product.name}")
    logger.info(f"URL адрес: {product.url}")
    logger.info(f"Цена: {product.price}")
    logger.info(f"Количество оценок: {product.avg_grade}")
    logger.info(f"Средняя оценка: {product.num_of_grades}")
    logger.info(f"Изменение цены за все время: {diff_price}")
    logger.info(f"Средняя цена за все время: {avg_price}")
