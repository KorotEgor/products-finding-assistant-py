from products_assistent.DB.conn_to_db import DBConnectionMixin

class ProductsTable(DBConnectionMixin):
    def create_table_products(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                url VARCHAR(255) NOT NULL,
                price INTEGER NOT NULL,
                avg_grade INTEGER NOT NULL,
                num_of_grades REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            )
            """)

    def save_product(self, product):
        name = product.name
        url = product.url
        price = product.price
        avg_grade = product.avg_grade
        num_of_grades = product.num_of_grades
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                    INSERT INTO products (name, url, price, avg_grade, num_of_grades)
                    VALUES (?, ?, ?, ?, ?)
                """,
                (name, url, price, avg_grade, num_of_grades,),
            )

    def get_product_by_name(self, name):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT name, url, price, avg_grade, num_of_grades
                FROM products
                WHERE name = ?
            """,
                (name,),
            )
            product = cur.fetchone()

        return product

    def update_product(self, name, new_price, new_avg_grade, new_num_of_grades):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE products SET
                    price = ?,
                    avg_grade = ?,
                    num_of_grades = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE name = ?
                """,
                (new_price, new_avg_grade, new_num_of_grades, name,)
            )
