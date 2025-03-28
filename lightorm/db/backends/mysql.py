
from lightorm.db.backends.base import Database


class MySQLDatabase(Database):
    def __init__(self, config):
        super().__init__(config)

    def connect(self):
        import mysql.connector
        self._connection = mysql.connector.connect(**self._config)
        return self._connection

    def disconnect(self):
        if self._connection:
            self._connection.close()

    def execute(self, query, params=None):
        with self._connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, params or ())
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            self._connection.commit()
            return cursor.lastrowid

    def begin_transaction(self):
        """Begin transaction."""
        self._connection.start_transaction()

    def commit_transaction(self):
        """Commit transaction."""
        self._connection.commit()

    def rollback_transaction(self):
        """Rollback transaction."""
        self._connection.rollback()