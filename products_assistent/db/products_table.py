from products_assistent.db.conn_to_db import DBConnectionMixin
from products_assistent import products


class ProductsRepo(DBConnectionMixin):
    def __init__(self, db_path):
        super().__init__(db_path)

    def create_table_products(self):
        with self.get_connection() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                url VARCHAR(255) NOT NULL,
                price INTEGER NOT NULL,
                avg_grade INTEGER NOT NULL,
                num_of_grades REAL NOT NULL,
            )
            """)

    def save_product(self, product):
        name = product.name
        url = product.url
        price = product.price
        avg_grade = product.avg_grade
        num_of_grades = product.num_of_grades
        with self.get_connection() as conn:
            conn.execute(
                """
                    INSERT INTO products (name, url, price, avg_grade, num_of_grades)
                    VALUES (?, ?, ?, ?, ?)
                """,
                (
                    name,
                    url,
                    price,
                    avg_grade,
                    num_of_grades,
                ),
            )

    def get_product_by_name(self, name):
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                SELECT name, url, price, avg_grade, num_of_grades
                FROM products
                WHERE name = ?
            """,
                (name,),
            )
            product = cur.fetchone()

        if product is None:
            return None

        return products.Product(*product)

    def update_product(self, name, new_price, new_avg_grade, new_num_of_grades):
        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE products SET
                    price = ?,
                    avg_grade = ?,
                    num_of_grades = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE name = ?
                """,
                (
                    new_price,
                    new_avg_grade,
                    new_num_of_grades,
                    name,
                ),
            )
