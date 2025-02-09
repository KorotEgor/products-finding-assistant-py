from datetime import datetime

from products_assistent.db.conn_to_db import DBConnectionMixin
from products_assistent import products

from dataclasses import dataclass


@dataclass
class DBProduct(products.Product):
    id: int
    date: datetime


class ProductsRepo(DBConnectionMixin):
    def __init__(self, db_path):
        super().__init__(db_path)

    def create_table_products(self):
        with self.get_connection() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                request_id INTEGER NOT NULL,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                price INTEGER NOT NULL,
                avg_grade REAL NOT NULL,
                num_of_grades INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY (request_id) REFERENCES requests (id) ON DELETE CASCADE
            )
            """)

    def save_product(self, req_id, product):
        name = product.name
        url = product.url
        price = product.price
        avg_grade = product.avg_grade
        num_of_grades = product.num_of_grades
        with self.get_connection() as conn:
            cur = conn.execute(
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

        return id

    def get_dbproduct_by_req(self, req):
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                SELECT prd.name, prd.url, prd.price, prd.avg_grade, prd.num_of_grades, prd.id, prd.created_at
                FROM products AS prd
                LEFT JOIN requests AS req
                ON req.id = prd.request_id
                WHERE req.request = ?
            """,
                (req,),
            )
            product = cur.fetchone()

        if product is None:
            return None

        return DBProduct(*product[:-1], datetime.fromisoformat(product[-1]))

    def get_diff_avg_price_by_prd_id(self, prd_id):
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                        SELECT MIN(price), MAX(price), AVG(price)
                        FROM products
                        WHERE id = ?
                    """,
                (prd_id,),
            )
            min_price, max_price, avg_price = cur.fetchone()

        return max_price - min_price, avg_price
