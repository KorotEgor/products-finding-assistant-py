from products_assistent.db.conn_to_db import DBConnectionMixin


class RequestsRepo(DBConnectionMixin):
    def __init__(self, db_path):
        super().__init__(db_path)

    def create_table_requests(self):
        with self.get_connection() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY,
                request VARCHAR(255) UNIQUE NOT NULL
            )
            """)

    def save_request(self, request):
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                    INSERT INTO requests (request)
                    VALUES (?)
                """,
                (request,),
            )
            id = cur.lastrowid

        return id
