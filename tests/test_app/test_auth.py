def test_register_created_user(client):
    response = client.post(
        "/auth/register",
        data={
            "username": "test_name",
            "email": "test_email@gmail.com",
            "password": "Test_pass123!",
        },
    )

    assert response.status_code == 302

    assert response.headers["Location"] == "/auth/register"


def test_register_right(client):
    assert client.get('/auth/register').status_code == 200

    response = client.post(
        "/auth/register",
        data={
            "username": "test_name",
            "email": "test_email@gmail.right",
            "password": "Test_pass123!",
        },
    )

    assert response.status_code == 302

    assert response.headers["Location"] == "/"
