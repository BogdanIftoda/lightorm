from lightorm.fields.base import Field
from lightorm.fields.integer import IntegerField


class ModelMeta(type):

    def __new__(cls, name, bases, attrs):
        fields = {}
        for field_name, field in attrs.items():
            if isinstance(field, Field):
                fields[field_name] = field

        if not any(field.primary_key for field in fields.values()):
            fields["id"] = IntegerField(primary_key=True, auto_increment=True)

        attrs["_fields"] = fields
        attrs["__tablename__"] = attrs.get("__tablename__", name.lower())

        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def set_executor(cls, executor):
        cls._executor = executor
