import sqlite3


class DBConnectionMixin:
    def get_connection(self):
        return sqlite3.connect("products_assistent.db")
