"""
This file will contain the different configs used by
different databases.

We can also add some helper functions to form urls
db urls and stuff
"""

from enum import Enum

from pydantic import BaseModel


class AvailableDatabases(Enum):
    mysql = "MySQL"
    postgres = "PostgreSQL"
    sqlite = "SQLite"
    mariadb = "MariaDB"
    oracle = "Oracle"


class PostgresConfig(BaseModel):
    """
    This class will be used to store the configs for the postgres database.
    """

    db_type: AvailableDatabases = AvailableDatabases.postgres
    host: str
    port: int
    username: str
    password: str
    database: str

    def get_db_url(self):
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class MySQLConfig(BaseModel):
    """
    This class will be used to store the configs for the mysql database.
    """

    db_type: AvailableDatabases = AvailableDatabases.mysql
    host: str
    port: int
    username: str
    password: str
    database: str

    def get_db_url(self):
        return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class SQLiteConfig(BaseModel):
    """
    This class will be used to store the configs for the
    sqlite database.
    """

    db_type: AvailableDatabases = AvailableDatabases.sqlite

    database: str

    def get_db_url(self):
        return f"sqlite:///{self.database}"


class MariaDBConfig(BaseModel):
    """
    This class will be used to store the configs for the mariadb database.
    """

    db_type: AvailableDatabases = AvailableDatabases.mariadb
    host: str
    port: int
    username: str
    password: str
    database: str

    def get_db_url(self):
        return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class OracleConfig(BaseModel):
    """
    This class will be used to store the configs for the oracle database.
    """

    db_type: AvailableDatabases = AvailableDatabases.oracle
    host: str
    port: int
    username: str
    password: str
    database: str

    def get_db_url(self):
        return f"oracle://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


DATABASE_CONFIGS = {
    AvailableDatabases.mysql: MySQLConfig,
    AvailableDatabases.postgres: PostgresConfig,
    AvailableDatabases.sqlite: SQLiteConfig,
    AvailableDatabases.mariadb: MariaDBConfig,
    AvailableDatabases.oracle: OracleConfig,
}
