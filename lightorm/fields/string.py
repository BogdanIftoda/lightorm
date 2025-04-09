from lightorm.fields.base import Field


class StringField(Field):
    _field_type = str

    def __init__(self, required=False, default=None, max_length=None, primary_key=False):
        super().__init__(required, default, primary_key)
        self._validate_concrete_type(max_length, int)
        self._max_length = max_length
        self._sql_type = f"VARCHAR({max_length})"

    def validate(self, value):
        super().validate(value)
        if value is None and not self._required:
            return
        if self._max_length is not None and len(value) > self._max_length:
            raise ValueError(
                f"Field '{self._name}' exceeds max_length {self._max_length}"
            )
