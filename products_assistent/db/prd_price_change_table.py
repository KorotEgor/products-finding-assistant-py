from products_assistent.db.conn_to_db import DBConnectionMixin


class PoductsrdPricesRepo(DBConnectionMixin):
    def __init__(self, db_path):
        super().__init__(db_path)

    def create_table_prd_prices(self):
        with self.get_connection() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS products_prices (
                id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                price INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
            )
            """)

    # https://sqlite.org/forum/info/2272562b935e3f82
    def get_min_max_avg_price_by_prd_id(self, prd_id):
        with self.get_connection() as conn:
            min_price = conn.execute(
                """
                    SELECT MIN(price)
                    FROM products_prices
                    WHERE product_id = ?
                """,
                (prd_id,),
            ).fetchone()
            max_price = conn.execute(
                """
                    SELECT MAX(price)
                    FROM products_prices
                    WHERE product_id = ?
                """,
                (prd_id,),
            ).fetchone()
            avg_price = conn.execute(
                """
                    SELECT AVG(price)
                    FROM products_prices
                    WHERE product_id = ?
                """,
                (prd_id,),
            ).fetchone()

        return *min_price, *max_price, *avg_price

    def save_prd_price(self, prd_id, prd_price):
        with self.get_connection() as conn:
            conn.execute(
                """
                    INSERT INTO products_prices (product_id, price)
                    VALUES (?, ?)
                """,
                (
                    prd_id,
                    prd_price,
                ),
            )
