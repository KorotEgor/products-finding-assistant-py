from products_assistent.products import get_products_list
from products_assistent.choice_alg import get_leaderboard
# sony wh-1000xm4
# logitech g435
# playstation 5
PRODUCT = "steamdeck"


def show_data():
    url = "https://market.yandex.ru/search?text=" + "%20".join(PRODUCT.split())
    products = get_products_list(url)

    if len(products) == 0:
        print("Нет сильно отличающихся вариантов")
        return

    best_products = get_leaderboard(products, PRODUCT)

    for product in best_products:
        print(product)

if __name__ == "__main__":
    show_data()
