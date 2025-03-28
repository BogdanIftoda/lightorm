from abc import ABC, abstractmethod

class Database(ABC):
    def __init__(self, config):
        self._config = config

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def execute(self, query, params=None):
        pass

    @abstractmethod
    def begin_transaction(self):
        """Begin a transaction."""
        pass

    @abstractmethod
    def commit_transaction(self):
        """Commit the current transaction."""
        pass

    @abstractmethod
    def rollback_transaction(self):
        """Rollback the current transaction."""
        pass