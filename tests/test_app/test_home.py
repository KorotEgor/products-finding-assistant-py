def test_home(client, app):
    err_test = "статус кода не равен 200"
    assert client.get("/").status_code == 200, err_test

    response = client.post(
        "/",
        data={"product_req": "test_req"},
    )

    assert response.status_code == 200, err_test
