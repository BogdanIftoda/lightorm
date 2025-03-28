from lightorm.db.backends.base import Database


class SQLiteDatabase(Database):

    def __init__(self, config):
        super().__init__(config)
        self.connect()
    def connect(self):
        import sqlite3
        self._connection = sqlite3.connect(self._config["database"])
        self._connection.row_factory = sqlite3.Row
        # return self._connection

    def disconnect(self):
        if self._connection:
            self._connection.close()

    def execute(self, query, params=None):
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            if query.strip().upper().startswith("SELECT"):
                return [dict(row) for row in cursor.fetchall()]
            conn.commit()
            return cursor.lastrowid


    def begin_transaction(self):
        """Begin transaction."""
        self._connection.execute("BEGIN")

    def commit_transaction(self):
        """Commit transaction."""
        self._connection.commit()

    def rollback_transaction(self):
        """Rollback transaction."""
        self._connection.rollback()

    @property
    def connection(self):
        return self._connection