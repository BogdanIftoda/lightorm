from lightorm.db.backends.base import Database

class PostgreSQLDatabase(Database):
    def __init__(self, config):
        super().__init__(config)

    def connect(self):
        import psycopg2
        self._connection = psycopg2.connect(**self._config)
        return self._connection

    def disconnect(self):
        if self._connection:
            self._connection.close()

    def execute(self, query, params=None):
        import psycopg2.extras
        with self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query, params or ())
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            self._connection.commit()
            return cursor.rowcount


    def begin_transaction(self):
        """Begin transaction."""
        self._connection.autocommit = False

    def commit_transaction(self):
        """Commit transaction."""
        self._connection.commit()
        self._connection.autocommit = True

    def rollback_transaction(self):
        """Rollback transaction."""
        self._connection.rollback()