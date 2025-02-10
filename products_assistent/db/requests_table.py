from sqlite3 import DatabaseError


class RequestsRepo:
    def __init__(self, db):
        self.db = db

    def save_request(self, request):
        try:
            cur = self.db.execute(
                """
                    SELECT id FROM requests
                    WHERE request = ?
                """,
                (request,),
            )
            id = cur.fetchone()
            if id is not None:
                return id[0]

            cur = self.db.execute(
                """
                    INSERT INTO requests (request)
                    VALUES (?)
                """,
                (request,),
            )
            id = cur.lastrowid
        except DatabaseError as err:
            return err

        return id
