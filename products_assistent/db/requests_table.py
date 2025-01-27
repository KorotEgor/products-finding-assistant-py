from datetime import datetime

from products_assistent.db.conn_to_db import DBConnectionMixin
from products_assistent import products


class RequestsRepo(DBConnectionMixin):
    def __init__(self, db_path):
        super().__init__(db_path)

    def create_table_requests(self):
        with self.get_connection() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY,
                request VARCHAR(255) UNIQUE NOT NULL,
                product_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
            )
            """)

    def get_product_and_date_by_req(self, request):
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                SELECT prd.name, prd.url, prd.price, prd.avg_grade, prd.num_of_grades, req.updated_at
                FROM products AS prd
                LEFT JOIN requests AS req
                ON req.product_id = prd.id
                WHERE req.request = ?
            """,
                (request,),
            )
            product = cur.fetchone()

        if product is None:
            return None

        updated_at = product[-1]
        return products.Product(*product[:-1]), datetime.fromisoformat(updated_at)

    def save_request(self, request, product_id):
        with self.get_connection() as conn:
            conn.execute(
                """
                    INSERT INTO requests (request, product_id)
                    VALUES (?, ?)
                """,
                (
                    request,
                    product_id,
                ),
            )

    def update_request(self, request):
        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE requests SET
                    updated_at = CURRENT_TIMESTAMP
                WHERE request = ?
                """,
                (request,),
            )
    
    def get_get(self):
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                SELECT * FROM requests
            """,
            )
            a = cur.fetchall()
        return a