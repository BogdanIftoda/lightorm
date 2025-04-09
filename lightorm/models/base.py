from lightorm.meta.model_meta import ModelMeta


class Model(metaclass=ModelMeta):

    def __init__(self, **kwargs):
        for field_name, field in self._fields.items():

            value = kwargs.get(field_name, field.default)

            if value is None and field.required:
                raise ValueError(f"{field_name} is required.")

            field.validate(value)
            setattr(self, field_name, value)

    def to_dict(self):
        return {field_name: getattr(self, field_name) for field_name in self._fields}

    def __repr__(self):

        field_values = ", ".join(f"{k}={v}" for k, v in self.to_dict().items())
        return f"<{self.__class__.__name__}({field_values})>"

    @classmethod
    def create(cls, **fields):

        field_names = []
        values = []
        for field_name, field in cls._fields.items():
            if field.required and field_name not in fields:
                raise ValueError(f"{field_name} is required.")
            value = fields.get(field_name, field.default)
            field.validate(value)
            field_names.append(field_name)
            values.append(value)

        fields_str = ", ".join(field_names)
        placeholders = ", ".join(["?"] * len(values))  # Use `?` for SQLite
        query = f"INSERT INTO {cls.__tablename__} ({fields_str}) VALUES ({placeholders})"

        inserted_id = cls._executor.execute(query, tuple(values))
        if "id" in cls._fields and inserted_id:
            fields["id"] = inserted_id

        return cls(**fields)

    @classmethod
    def get(cls, pk):
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = %s LIMIT 1;"
        result = cls._executor.execute(query, (pk,), fetch_one=True)
        if not result:
            return None
        return cls(**result)

    @classmethod
    def update(cls, pk, **fields):

        if not pk:
            raise ValueError("Primary key is required for update.")

        field_updates = []
        values = []
        for field_name, field in cls._fields.items():
            if field_name in fields:
                value = fields[field_name]
                field.validate(value)
                field_updates.append(f"{field_name} = %s")
                values.append(value)

        if not field_updates:
            raise ValueError("No fields provided for update.")

        values.append(pk)

        field_updates_str = ", ".join(field_updates)
        query = f"UPDATE {cls.__tablename__} SET {field_updates_str} WHERE id = %s"

        rows_affected = cls._executor.execute(query, tuple(values))
        return rows_affected > 0

    @classmethod
    def delete(cls, pk):
        if not pk:
            raise ValueError("Primary key is required for delete.")

        query = f"DELETE FROM {cls._table_name} WHERE id = %s;"
        rows_affected = cls._executor.execute(query, (pk,))
        return rows_affected > 0

    @classmethod
    def init_db(cls, executor):

        cls._executor = executor

    @classmethod
    def create_table(cls):

        columns = []
        for field_name, field in cls._fields.items():
            column_definition = f"{field_name} {field.sql_type}"
            # Add constraints
            if field.primary_key:
                column_definition += " PRIMARY KEY"
            if field.unique:
                column_definition += " UNIQUE"
            if field.auto_increment:
                column_definition += " AUTOINCREMENT"
            if field.required:
                column_definition += " NOT NULL"

            columns.append(column_definition)

        columns_str = ", ".join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {cls.__tablename__} ({columns_str})"

        cls._executor.execute(query)
