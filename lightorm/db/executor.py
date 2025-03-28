class SQLExecutor:

    def __init__(self, database):
        self.database = database

    def execute(self, query, params=None, fetch_one=False):
        try:
            if query.strip().upper().startswith("SELECT"):
                if fetch_one or "LIMIT 1" in query.upper():
                    return self.fetch_one(query, params)
                return self.fetch_all(query, params)
            return self._execute_and_commit(query, params)
        except Exception as e:
            self.database.rollback_transaction()
            raise e

    def fetch_one(self, query, params=None):

        cursor = self.database.connection.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, query, params=None):

        cursor = self.database.connection.cursor()
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        cursor.close()
        return results

    def _execute_and_commit(self, query, params=None):

        cursor = self.database.connection.cursor()
        cursor.execute(query, params or ())
        self.database.commit_transaction()
        cursor.close()
        return cursor.rowcount
