from flask import session


def test_register_right(client):
    assert client.get('/auth/register').status_code == 200

    response = client.post(
        "/auth/register",
        data={
            "username": "test_name",
            "email": "test_email@gmail.right",
            "password": "Test_pass123!",
            "access_password": "Test_pass123!",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    response = client.post(
        "/auth/register",
        data={
            "username": "test_name",
            "email": "test_email@gmail.com",
            "password": "Test_pass123!",
            "access_password": "Test_pass123!",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/register"

    response = client.post(
        "/auth/register",
        data={
            "username": "test_name",
            "email": "test_email@gmail.com",
            "password": "Test_pass123!",
            "access_password": "wrong_pass",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/register"


def test_login_right(client):
    assert client.get('/auth/login').status_code == 200

    response = client.post(
        "/auth/login",
        data={
            "email": "test_email@gmail.com",
            "password": "Test_pass123!",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"


def test_login_wrong(client):
    response = client.post(
        "/auth/login",
        data={
            "email": "test_email@gmail.wrong",
            "password": "Test_pass123!",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/register"

    response = client.post(
        "/auth/login",
        data={
            "email": "test_email@gmail.com",
            "password": "wrong_pass",
        },
    )

    assert response.status_code == 200


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
