from lightorm.fields.base import Field


class IntegerField(Field):
    _field_type = bool

    def __init__(self, required=False, default=None, primary_key=False, auto_increment=False):
        super().__init__(required, default, primary_key, auto_increment)
        self._sql_type = "BOOLEAN"
