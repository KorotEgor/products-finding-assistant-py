import pytest
from bs4 import BeautifulSoup
import responses
# import requests

from products_assistent.yandex.products import (
    NoneProduct,
    CheckString,
    Product,
    get_product_cards,
    del_offer_feed_if_there_is,
    get_divs_with_data,
    get_name_and_rating,
    get_rating_divs,
    get_grades,
    get_avg_grades,
    get_price,
    get_url,
    create_product,
    get_right_products,
    get_html_file,
)


def test_none_product():
    none_product = NoneProduct()
    err_text = "не верно работает метод find"
    assert none_product.find("test") is none_product, err_text

    err_text = "не верно работает метод div"
    assert none_product.div("test") is none_product, err_text

    err_text = "не верно работает метод a"
    assert none_product.a("test") is none_product, err_text

    err_text = "не верно работает метод span"
    assert none_product.span("test") is none_product, err_text

    err_text = "не верно работает метод string"
    assert none_product.string("test") is none_product, err_text

    err_text = "не верно работает метод find_all"
    assert none_product.find_all("test") is none_product, err_text

    err_text = "не верно работает метод split"
    assert none_product.split("test") is none_product, err_text

    err_text = "не верно работает метод get"
    assert none_product.get("test") is none_product, err_text

    err_text = "не верно работает метод __getitem__"
    assert none_product[123] is none_product, err_text

    err_text = "не верно работает метод __add__"
    assert none_product + none_product is none_product, err_text


def test_check_string():
    check_string = CheckString("test")

    err_text = "не верно работает метод join с не list"
    assert isinstance(check_string.join("test"), NoneProduct), err_text

    err_text = "не верно работает метод join с list"
    join_string = check_string.join(["1", "2"])
    assert not isinstance(join_string, NoneProduct), err_text

    err_text = "не верно возращает значение с аргументом типа list"
    assert join_string == "1test2", err_text


@pytest.fixture
def prd_cards_soup():
    with open("tests/fixtures/yandex/prd_cards.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    return soup, soup.find("div", class_="bad")


def test_get_prd_cards(prd_cards_soup):
    right_test, err_test = (
        get_product_cards(prd_cards_soup[0]),
        prd_cards_soup[1],
    )
    err_text = "не возващает правильный результат"
    assert len(right_test) == 2, err_text

    with pytest.raises((UnboundLocalError, AttributeError)):
        get_product_cards(err_test)


@pytest.fixture
def del_offer_soup():
    with open("tests/fixtures/yandex/del_offer.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    return soup.find_all("div", recursive=False)


def test_del_offer_feed(del_offer_soup):
    (
        first_offer_test,
        second_offer_test,
        empty_dell_test,
        first_offer_class_test,
        second_offer_class_test,
    ) = del_offer_soup

    err_text = "не удаляет с атрибутом: @monetize/IncutConstructor/Premium"
    assert len(del_offer_feed_if_there_is([first_offer_test])) == 0, err_text

    err_text = "не удаляет с атрибутом: @monetize/PremiumIncut"
    assert len(del_offer_feed_if_there_is([second_offer_test])) == 0, err_text

    err_text = "удяляет даже, если data-apiary-widget-name не верный атрибут"
    assert len(del_offer_feed_if_there_is([empty_dell_test])) == 1, err_text

    err_text = "удяляет даже, если class=@monetize/IncutConstructor/Premium"
    assert len(del_offer_feed_if_there_is([first_offer_class_test])) == 1, (
        err_text
    )

    err_text = "удяляет даже, если class=@monetize/PremiumIncut"
    assert len(del_offer_feed_if_there_is([second_offer_class_test])) == 1, (
        err_text
    )


@pytest.fixture
def divs_with_data_soup():
    with open("tests/fixtures/yandex/divs_with_data.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    return soup.find_all("div", recursive=False)


def test_get_divs_with_data(divs_with_data_soup):
    none_test, recurs_test, class_test = divs_with_data_soup

    err_text = "не возващает None, когда надо"
    assert isinstance(get_divs_with_data(none_test), NoneProduct), err_text

    err_text = (
        "возващает div внутри div-ов или data-apiary-widget-name не проверяется"
    )
    assert len(get_divs_with_data(recurs_test)) == 2, err_text

    err_text = "возващает даже, если class=@marketfront/EmptyIncut"
    assert len(get_divs_with_data(class_test)) == 1, err_text


@pytest.fixture
def name_and_rating_soup():
    with open("tests/fixtures/yandex/name_and_rating.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    right_soup, wrong_soup = soup.find_all("div", recursive=False)
    return (0, right_soup), (0, wrong_soup)


def test_get_name_and_rating(name_and_rating_soup):
    right_soup, wrong_soup = name_and_rating_soup

    right_name, right_rating = get_name_and_rating(right_soup)
    err_text = "неверное имя"
    assert right_name == "right", err_text

    err_text = "неверный рейтинг"
    assert right_rating.string == "right", err_text

    wrong_name, wrong_rating = get_name_and_rating(wrong_soup)
    err_text = "не верно передает при отсутствии рейтинга имени"
    assert isinstance(wrong_name, NoneProduct), err_text

    err_text = "не верно передает при отсутствии рейтинга"
    assert isinstance(wrong_rating, NoneProduct), err_text


@pytest.fixture
def rating_divs_soup():
    with open("tests/fixtures/yandex/rating_divs.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    return soup


def test_get_rating_divs(rating_divs_soup):
    raiting = get_rating_divs(rating_divs_soup)

    err_text = "неверно находит рейтинг"
    assert len(raiting) == 2, err_text


@pytest.fixture
def grades_soup():
    with open("tests/fixtures/yandex/grades.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    return ("0", *soup.find_all("span"))


def test_get_grades(grades_soup):
    grades = get_grades(grades_soup)

    err_text = "не тот тип данных"
    assert isinstance(grades, int), err_text

    err_text = "не верное получение оценок"
    assert grades == 1, err_text

    err_text = "не верно работает с NoneProduct"
    assert isinstance(get_grades(NoneProduct()), NoneProduct), err_text


@pytest.fixture
def avg_grades_soup():
    with open("tests/fixtures/yandex/avg_grades.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    return (*soup.find_all("span"), "0")


def test_get_avg_grades(avg_grades_soup):
    avg_grades = get_avg_grades(avg_grades_soup)

    err_text = "не тот тип данных"
    assert isinstance(avg_grades, float), err_text

    err_text = "не верное получение средних оценок"
    assert avg_grades == 1.0, err_text

    err_text = "не верно работает с NoneProduct"
    assert isinstance(get_avg_grades(NoneProduct()), NoneProduct), err_text


@pytest.fixture
def price_soup():
    with open("tests/fixtures/yandex/price.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    return ("0", "0", soup)


def test_get_price(price_soup):
    price = get_price(price_soup)

    err_text = "не тот тип данных"
    assert isinstance(price, int), err_text

    err_text = "не верное получение цены"
    assert price == 1234, err_text


@pytest.fixture
def url_soup():
    with open("tests/fixtures/yandex/url.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    return (0, 0, 0, 0, soup), NoneProduct()


def test_get_url(url_soup):
    none_url, url = url_soup[-1], get_url("right.", *url_soup[:-1])

    err_text = "не верный url"
    assert url == "https://right.right", err_text

    err_text = "не возвращает NoneProduct при отсутствии url"
    assert none_url is url_soup[-1], err_text


@pytest.fixture
def get_attrs_for_prd():
    right_prd = ["right" for _ in range(5)]
    wrong_prds = []
    for i in range(3):
        wrong_prds.append(right_prd[:i] + [NoneProduct()] + right_prd[i + 1 :])

    return right_prd, *wrong_prds


def test_create_product(get_attrs_for_prd):
    right_prd, wrong_name_prd, wrong_url_prd, wrong_price_prd = get_attrs_for_prd

    err_text = "не верно создает продукт, когда все верно"
    assert Product(*right_prd) == create_product(*right_prd), err_text

    err_text = "не верно создает продукт, когда не верное имя"
    assert create_product(*wrong_name_prd) is None, err_text

    err_text = "не верно создает продукт, когда не верный url"
    assert create_product(*wrong_url_prd) is None, err_text

    err_text = "не верно создает продукт, когда не верная цена "
    assert create_product(*wrong_price_prd) is None, err_text


@pytest.fixture
def test_get_right_products():
    return (
        Product(
            name="right",
            url="https://right.right",
            price=1234,
            avg_grade=1.0,
            num_of_grades=1,
        ),
        NoneProduct(),
        None,
        [],
        "",
    )


def fake_prd_data(product_html, market_name):
    return product_html


def test_right_products(test_get_right_products):
    testing_products = get_right_products(
        test_get_right_products, "yandex", get_prd_data=fake_prd_data
    )
    right_product = test_get_right_products[0]

    err_text = "не верное количество возвращаемых продуктов"
    assert len(testing_products) == 1, err_text

    err_text = "не верный возвращаемых продукт"
    assert testing_products[0] is right_product, err_text


@pytest.fixture
def get_test_html():
    with open("tests/fixtures/yandex/test_html.html", "r") as f:
        return f.read()


@responses.activate
def test_get_html_file(get_test_html):
    test_html = get_test_html
    responses.add(
        responses.GET,
        "https://test/search/?text=test%20first",
        body=test_html,
        status=200,
    )
    # не знаю как спровоцировать такое поведение
    # with pytest.raises(requests.exceptions.RequestException):
    #     resp = get_html_file(
    #         product_name="",
    #         market_name="",
    #     )
    resp = get_html_file(product_name="test first", market_name="test")

    err_text = "вернул не BeautifulSoup"
    assert isinstance(resp, BeautifulSoup), err_text

    err_text = "вернул не верные данные с сайта"
    assert resp == BeautifulSoup(test_html, "html.parser"), err_text

    responses.add(
        responses.GET,
        "https://test/search/?text=test%20first",
        body=test_html,
        status=404,
    )
    resp = get_html_file()

    err_text = "вернул не None при плохом коде ответа"
    assert resp is None, err_text
