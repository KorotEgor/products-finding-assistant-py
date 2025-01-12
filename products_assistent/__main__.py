import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

PRODUCT = "sony wh-1000xm4"


@dataclass
class Product:
    name: str
    url: str
    price: int
    avg_grade: float
    num_of_grades: int


# Здесь ты получаешь строку с текстом и ценой. Таких вариантов строк 2, поэтому так
# Цена с картой Яндекс Пэй 23 750 ₽ вместо 23 990
# Цена 25 650 ₽
def to_cor_num(string):
    s = string.split()
    if len(s) > 7:
        x = (len(s) - 7) // 2
        num = int(''.join(s[7 + x:]))
    else:
        num = int(''.join(s[1:-1]))

    return num


def get_product(product_html):
    data = product_html.div.article.div
    if data.get("data-apiary-widget-name") == "@marketfront/EmptyIncut":
        return False
    data = data.div.div.div.find_all("div", recursive=False)

    name_rating_url = data[1]

    name_url = name_rating_url.find("div", attrs={"data-baobab-name": "title"}, recursive=False).div.a
    url = name_url["href"]
    name = name_url.span.string

    rating = name_rating_url.find("div", attrs={"data-baobab-name": "rating"}, recursive=False)
    if rating is not None:
        rating = rating.find_all("span", recursive=False)
        avg_grade = float(rating[0].string.split()[2])
        grades = int(rating[1].string.split()[2])
    else:
        avg_grade = 0.0
        grades = 0

    price = to_cor_num(data[2].div.div.div.a.div.span.string)

    return Product(
        name=name,
        url=url,
        price=price,
        avg_grade=avg_grade,
        num_of_grades=grades,
    )


def find_best_product():
    url = "https://market.yandex.ru/search?text=" + "%20".join(PRODUCT.split())
    try:
        request = requests.get(
            url,
            headers={"User-Agent": "page_analyzer"},
        )
    except requests.exceptions.RequestException:
        print("Error with request")

    soup = BeautifulSoup(request.text, "html.parser")
    products_html = soup.find(
        "div",
        class_="serverList-item",
    ).find_all("div", recursive=False)

    offer_feed = products_html[0].find("div")
    offer_feeds = ("@monetize/IncutConstructor/Premium", "@monetize/PremiumIncut")
    if offer_feed.get("data-apiary-widget-name") in offer_feeds:
        products_html = products_html[1:]

    products = []
    for product_html in products_html:
        product = get_product(product_html)
        if product:
            print(product.price)
            products.append(products)

    print(products[0])


if __name__ == "__main__":
    find_best_product()
