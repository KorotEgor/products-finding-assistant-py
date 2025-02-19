import pytest
from bs4 import BeautifulSoup

from products_assistent.products import get_product_cards, del_offer_feed_if_there_is


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
            err_text = 'не выбрасывает ошибку при отсутствии карт'
        assert pass_test, err_text


@pytest.fixture
def del_offer_soup():
    with open("tests/fixtures/yandex/del_offer.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    return soup.find_all("div", recursive=False)


def test_del_offer_feed(del_offer_soup):
    soup_array = del_offer_soup
    print(soup_array[2].div.get("data-apiary-widget-name") == "@monetize/PremiumIncut")

    try:
        first_test = del_offer_feed_if_there_is([soup_array[0]])
    except IndexError:
        err_text = 'берет не первых эллемент'
        assert True, err_text

    err_text = "не удаляет с атрибутом: @monetize/IncutConstructor/Premium"
    assert len(first_test) == 0, err_text

    err_text = "не удаляет с атрибутом: @monetize/PremiumIncut"
    assert len(del_offer_feed_if_there_is([soup_array[1]])) == 0, err_text

    err_text = "удяляет даже, если это не список предложений"
    assert len(del_offer_feed_if_there_is([soup_array[2]])) == 1, err_text

    err_text = "удяляет даже, если это не список предложений"
    assert len(del_offer_feed_if_there_is([soup_array[3]])) == 1, err_text


def fake_get_html_file(session, product_name, market_name):
    pass


def test_get_products_list():
    pass
