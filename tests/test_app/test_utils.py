from products_assistent.app.utils import (
    check_username,
    check_email,
    check_password,
)


def test_check_username():
    test = check_username("")
    assert len(test) == 1
    assert test[0] == "Это обязательное поле"

    assert len(check_username("test@test.com")) == 0


def test_check_email():
    assert len(check_email("test@test.com")) == 0

    test = check_email("")
    assert len(test) == 1
    assert "Это обязательное поле" in test

    test = check_email(" ")
    assert len(test) == 3
    assert 'В почте должен быть символ "@"' in test
    assert (
        'В почте должен быть символ ".", но он не должен идти после "@" и быть последним'
        in test
    )
    assert 'Почта должна содержать еще символы, кроме "@" и "."' in test

    test = check_email("test@test.")
    assert len(test) == 1
    assert (
        test[0]
        == 'В почте должен быть символ ".", но он не должен идти после "@" и быть последним'
    )

    test = check_email("test@.com")
    assert len(test) == 1
    assert (
        test[0]
        == 'В почте должен быть символ ".", но он не должен идти после "@" и быть последним'
    )


def test_check_password():
    print("Test123!".isdigit())
    assert len(check_password("Test123!")) == 0

    test = check_password("")
    assert len(test) == 1
    assert "Это обязательное поле" in test

    test = check_password(" ")
    assert len(test) == 5
    assert "Длина пароля должна быть больше или равна 8" in test
    assert "В пароле должны быть цифры" in test
    assert "В пароле должны быть большие буквы" in test
    assert "В пароле должны быть маленькие буквы" in test
    assert "В пароле должны быть специальные символы" in test
