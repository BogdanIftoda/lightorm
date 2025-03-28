from abc import ABC


class Field(ABC):
    _field_type = None

    def __init__(self, required=False, default=None, primary_key=False, auto_increment=False, unique=False):
        self._name = None
        self._validate_type(default)
        self._validate_concrete_type(required, bool)
        self._validate_concrete_type(primary_key, bool)
        self._validate_concrete_type(auto_increment, bool)
        self._validate_concrete_type(unique, bool)
        self._required = required
        self._default = default
        self._primary_key = primary_key
        self._auto_increment = auto_increment
        self._unique = unique

    def __set_name__(self, owner, name):
        self._name = name

    def _validate_type(self, value):
        return self._validate_concrete_type(value, self._field_type)

    @staticmethod
    def _validate_concrete_type(value, field_type):
        if value is not None and not isinstance(value, field_type):
            raise TypeError(f"Expected {field_type}, got {type(value).__name__}")

    def validate(self, value):
        self._validate_type(value)
