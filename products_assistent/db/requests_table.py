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
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
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
        return products.Product(*product[:-1]), updated_at

