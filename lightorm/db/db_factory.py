from lightorm.db.executor import SQLExecutor
from lightorm.meta.model_meta import ModelMeta


class DatabaseFactory:

    @staticmethod
    def init_db(config):
        db_type = config.get("type")
        try:
            if db_type == "mysql":
                from lightorm.mysql_database import MySQLDatabase
                connection = MySQLDatabase(config)
            elif db_type == "postgresql":
                from lightorm.db.postgresql_database import PostgreSQLDatabase
                connection = PostgreSQLDatabase(config)
            elif db_type == "sqlite":
                from lightorm.db.backends.sqlite import SQLiteDatabase
                connection = SQLiteDatabase(config)
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
            ModelMeta.set_executor(SQLExecutor(connection))
        except ImportError as e:
            raise ImportError(
                f"Missing required package for {db_type}. Please install using: "
                f"`pip install lightorm[{db_type}]`"
            )
