from setuptools import setup, find_packages

setup(
    name="lightorm",
    version="1.0.0",
    description="Lightweight ORM with multi-database support (MySQL, PostgreSQL, SQLite)",
    author="Bogdan Iftoda",
    author_email="your_email@example.com",
    url="https://github.com/BogdanIftoda/lightorm",
    packages=find_packages(),
    extras_require={
        "mysql": ["mysql-connector-python"],
        "postgresql": ["psycopg2-binary"],
        "sqlite": ["pysqlite3"],
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
