import sqlite3

from lightorm.db.db_factory import DatabaseFactory
from lightorm.fields.integer import IntegerField
from lightorm.fields.string import StringField
from lightorm.models.base import Model

db_config = {
    "database": "lightorm",
    "type": "sqlite",
}

# Initialize DB Once
DatabaseFactory.init_db(db_config)


class User(Model):
    __tablename__ = "user"

    name = StringField(max_length=100, required=True)
    age = IntegerField(min_value=18, required=True)


# Create a new record
user = User.create(name="John Doe", age=30)
print(f"User created: {user}")

# Retrieve a record
retrieved_user = User.get(1)
print(f"User found: {retrieved_user}" if retrieved_user else "User not found.")

# Update a record
User.update(pk=1, name="Johnny", age=35)

# Delete a record
User.delete(pk=1)
