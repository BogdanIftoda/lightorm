from .base import Field


class IntegerField(Field):
    _field_type = int

    def __init__(self, required=False, default=None, min_value=None, max_value=None, primary_key=False,
                 auto_increment=False):
        super().__init__(required, default, primary_key, auto_increment)
        self._validate_type(min_value)
        self._validate_type(max_value)
        self._min_value = min_value
        self._max_value = max_value
        self._sql_type = "INTEGER"

    def validate(self, value):
        super().validate(value)
        if value is None and not self._required:
            return
        if self._min_value is not None and value < self._min_value:
            raise ValueError(
                f"Field '{self._name}' must be greater than or equal to {self._min_value}"
            )
        if self._max_value is not None and value > self._max_value:
            raise ValueError(
                f"Field '{self._name}' must be less than or equal to {self._max_value}"
            )
