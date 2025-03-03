# from products_assistent.db import products_table
# from products_assistent.db.conn_to_db import get_db


# def test_save_product(app):
#     with app.app_context():
#         db = get_db()
#         reqs_repo = products_table.ProductsRepo(db)

#         err_text = " не верно вернул id уже сохраненного запроса"
#         assert reqs_repo.save_request("test_req1") == 1, err_text

#         err_text = "не верно вернул id запроса"
#         assert reqs_repo.save_request("test_req2") == 2, err_text

#         err_text = "не сохранил запрос"
#         assert db.execute(
#             "SELECT COUNT(*) FROM requests",
#         ).fetchone() == (2,), err_text