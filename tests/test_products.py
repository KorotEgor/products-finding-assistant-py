import pytest
from bs4 import BeautifulSoup

from products_assistent.products import (
    get_product_cards,
    del_offer_feed_if_there_is,
    get_divs_with_data,
    get_name_and_rating,
    get_rating_divs,
    get_grades,
)


@pytest.fixture
def prd_cards_soup_err():
    with open("tests/fixtures/yandex/prd_cards_err.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    return soup


def test_get_prd_cards_err(prd_cards_soup_err):
    pass_test = False
    soup = prd_cards_soup_err

    try:
        get_product_cards(soup)
    except (UnboundLocalError, AttributeError):
        pass_test = True
    finally:
        if not pass_test:
            err_text = "не выбрасывает ошибку при отсутствии карт"
        assert pass_test, err_text


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

    try:
        first_test = del_offer_feed_if_there_is([first_offer_test])
    except IndexError:
        err_text = "берет не первых эллемент"
        assert True, err_text

    err_text = "не удаляет с атрибутом: @monetize/IncutConstructor/Premium"
    assert len(first_test) == 0, err_text

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
    assert get_divs_with_data(none_test) is None, err_text

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

    return (0, *soup.find_all("span"))


def test_get_grades(grades_soup):
    grades = get_grades(grades_soup)

    err_text = "не тот тип данных"
    assert isinstance(grades, int), err_text

    err_text = "не верный получение оценок"
    assert grades == 1, err_text


def fake_get_html_file(session, product_name, market_name):
    pass


def test_get_products_list():
    pass
