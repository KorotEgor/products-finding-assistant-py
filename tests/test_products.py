import pytest
from bs4 import BeautifulSoup
import requests
import responses

from products_assistent.products import (
    get_product_cards,
    del_offer_feed_if_there_is,
    get_divs_with_data,
    get_name_and_rating,
    get_rating_divs,
    get_grades,
    get_avg_grades,
    get_price,
    get_url,
    get_html_file,
)
from products_assistent.products import NoneProduct


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

    return (0, soup)


def test_get_name_and_rating(name_and_rating_soup):
    raiting, name = get_name_and_rating(name_and_rating_soup)

    err_text = "неверное имя"
    assert name == "right", err_text

    err_text = "неверный рейтинг"
    assert raiting.string == "right", err_text


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

    return 0, 0, 0, 0, soup


def test_get_url(url_soup):
    url = get_url("right.", url_soup)

    err_text = "не верный url"
    assert url == "https://right.right", err_text


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
