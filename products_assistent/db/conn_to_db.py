import sqlite3


class DBConnectionMixin:
    def __init__(self, db_path):
        self._db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self._db_path)
