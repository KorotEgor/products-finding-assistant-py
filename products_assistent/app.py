from flask import Blueprint, render_template, request

from products_assistent import yandex
from products_assistent.db import products_table
from products_assistent.db import requests_table
from products_assistent.db import conn_to_db

bp = Blueprint("main", __name__)


@bp.route("/", methods=("GET", "POST"))
def home_view():
    product, diff_price, avg_price = "first", "", ""
    if request.method == "POST":
        product_req = request.form["product_req"]

        db = conn_to_db.get_db()
        products_repo = products_table.ProductsRepo(db)
        requests_repo = requests_table.RequestsRepo(db)
        product, diff_price, avg_price = yandex.get_product_data(
            product_req,
            products_repo,
            requests_repo,
        )

    return render_template(
        "home.html",
        product=product,
        diff_price=diff_price,
        avg_price=avg_price,
    )
