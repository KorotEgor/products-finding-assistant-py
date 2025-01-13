from time import sleep
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    url: str
    price: int
    avg_grade: float
    num_of_grades: int
    gen_grade: int


def get_product(product_html):
    data = product_html.div.article.div
    if data.get("data-apiary-widget-name") == "@marketfront/EmptyIncut":
        return None
    data = data.div.div.div.find_all("div", recursive=False)

    name_rating = data[1]

    name = name_rating.find(
        "div", attrs={"data-baobab-name": "title"}, recursive=False
    ).div.a
    name = name.span.string

    rating = name_rating.find(
        "div", attrs={"data-baobab-name": "rating"}, recursive=False
    )
    if rating is not None:
        rating = rating.find_all("span", recursive=False)

        grades = int(rating[1].string.split()[2])
        if grades == 0:
            return None

        avg_grade = float(rating[0].string.split()[2])
        gen_grade = round(grades * avg_grade)
    else:
        return None

    price = int(''.join(data[2].div.div.div.a.div.div.span.span.span.string.split()))

    # split для уменьшения размера url, так как ост не обезательное
    url = "https://market.yandex.ru" + data[4].a.get("href")

    return Product(
        name=name,
        url=url,
        price=price,
        avg_grade=avg_grade,
        num_of_grades=grades,
        gen_grade=gen_grade,
    )


def get_products_list(url):
    try:
        request = requests.get(
            url,
            headers={"User-Agent": "page_analyzer"},
        )
    except requests.exceptions.RequestException:
        print("Ошибка запроса")

    soup = BeautifulSoup(request.text, "html.parser")

    while True:
        try:
            products_html = soup.find(
                "div",
                class_="serverList-item",
            ).find_all("div", recursive=False)
        except AttributeError:
            print("Тебе нужен аккаунт яндекс маркета, чтобы приложение работало")
        finally:
            break

    offer_feed = products_html[0].find("div")
    offer_feeds = ("@monetize/IncutConstructor/Premium", "@monetize/PremiumIncut")
    if offer_feed.get("data-apiary-widget-name") in offer_feeds:
        products_html = products_html[1:]

    products = []
    for product_html in products_html:
        product = get_product(product_html)
        if product is not None:
            products.append(product)

    return products
