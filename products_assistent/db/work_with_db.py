import logging

logger = logging.getLogger(__name__)


def manage_to_save_to_db(products_repo, reqs_repo, product, req):
    req_id = reqs_repo.save_request(req)
    if isinstance(req_id, Exception):
        logger.error("Ошибка при сохранении в базу requests: %s", req_id)
        return None

    prd_id = products_repo.save_product(req_id, product)
    if isinstance(req_id, Exception):
        logger.error("Ошибка при сохранении в базу products: %s", prd_id)
        return None

    return prd_id
