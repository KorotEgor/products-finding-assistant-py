import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Product:
    name: str
    url: str
    price: int
    avg_grade: float
    num_of_grades: int


def get_divs_with_data(product_html):
    divs_data = product_html.div.article.div
    if divs_data.get("data-apiary-widget-name") == "@marketfront/EmptyIncut":
        return None

    return divs_data.div.div.div.find_all("div", recursive=False)


def get_name_and_rating(divs_data):
    name_rating = divs_data[1]

    name = name_rating.find(
        "div", attrs={"data-baobab-name": "title"}, recursive=False
    ).div.a
    name = name.span.string

    rating = name_rating.find(
        "div", attrs={"data-baobab-name": "rating"}, recursive=False
    )
    return rating, name


def get_rating_divs(rating):
    return rating.find_all("span", recursive=False)


def get_grades(rating):
    return int(rating[1].string.split()[2])


def get_avg_grades(rating):
    return float(rating[0].string.split()[2])


def get_price(divs_data):
    return int(
        "".join(
            divs_data[2].div.div.div.a.div.div.span.span.span.string.split(),
        )
    )


def get_url(market_name, divs_data):
    return "https://" + market_name + divs_data[4].a.get("href")


def get_product_data(product_html, market_name):
    divs_data = get_divs_with_data(product_html)
    if divs_data is None:
        return None

    rating, name = get_name_and_rating(divs_data)
    if rating is not None:
        rating = get_rating_divs(rating)

        grades = get_grades(rating)
        if grades == 0:
            return None

        avg_grade = get_avg_grades(rating)
    else:
        return None

    price = get_price(divs_data)

    url = get_url(market_name, divs_data)

    return Product(
        name=name,
        url=url,
        price=price,
        avg_grade=avg_grade,
        num_of_grades=grades,
    )


def get_product_cards(soup):
    return soup.find(
        "div",
        class_="serverList-item",
    ).find_all("div", recursive=False)


def del_offer_feed_if_there_is(products_html):
    offer_feed = products_html[0].find("div")

    offer_feeds = (
        "@monetize/IncutConstructor/Premium",
        "@monetize/PremiumIncut",
    )
    if offer_feed.get("data-apiary-widget-name") in offer_feeds:
        return products_html[1:]

    return products_html


def get_products_list(session, product_name, market_name):
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
            "application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Host": "market.yandex.ru",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/83.0.4103.61 Safari/537.36",
        }
        response = session.get(
            f"https://{market_name}/search/",
            headers=headers,
            params={"text": product_name},
        )
    except requests.exceptions.RequestException:
        logger.error("Ошибка запроса")
        return None

    if not response.ok:
        logger.error("Плохой код ответа")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        products_and_offers_html = get_product_cards(soup)
    except (UnboundLocalError, AttributeError) as err:
        logger.error("Ошибка при получении товара")
        return err

    products_html = del_offer_feed_if_there_is(products_and_offers_html)

    products = []
    for product_html in products_html:
        product = get_product_data(product_html, market_name)
        if product is not None:
            products.append(product)

    return products
