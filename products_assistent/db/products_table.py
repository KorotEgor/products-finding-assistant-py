from dataclasses import dataclass
from datetime import datetime
from sqlite3 import DatabaseError

from products_assistent import products


@dataclass
class DBProduct(products.Product):
    id: int
    date: datetime


class ProductsRepo:
    def __init__(self, db):
        self.db = db

    def save_product(self, req_id, product):
        name = product.name
        url = product.url
        price = product.price
        avg_grade = product.avg_grade
        num_of_grades = product.num_of_grades
        try:
            cur = self.db.execute(
                """
                    INSERT INTO products (request_id, name, url, price, avg_grade, num_of_grades)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    req_id,
                    name,
                    url,
                    price,
                    avg_grade,
                    num_of_grades,
                ),
            )
            id = cur.lastrowid
            self.db.commit()
        except DatabaseError as err:
            return err

        return id

    def get_dbproduct_by_req(self, req):
        try:
            cur = self.db.execute(
                """
                SELECT prd.name, prd.url, prd.price, prd.avg_grade, prd.num_of_grades, prd.id, prd.created_at as date
                FROM products AS prd
                LEFT JOIN requests AS req
                ON req.id = prd.request_id
                WHERE req.request = ?
                ORDER BY date desc
                LIMIT 1
            """,
                (req,),
            )
            product = cur.fetchone()
        except DatabaseError as err:
            return err

        if product is None:
            return None

        return DBProduct(*product[:-1], product[-1])

    def get_diff_avg_price_by_prd_id(self, req):
        try:
            cur = self.db.execute(
                """
                    SELECT MIN(prd.price), MAX(prd.price), AVG(prd.price)
                    FROM products AS prd
                    LEFT JOIN requests AS req
                    ON prd.request_id = req.id
                    WHERE req.request = ?
                """,
                (req,),
            )
            min_price, max_price, avg_price = cur.fetchone()

            if min_price is None:
                return None

        except DatabaseError as err:
            return err

        return max_price - min_price, avg_price
