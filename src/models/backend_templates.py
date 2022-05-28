"""
This file will be used to store the backend tempalte config structures required 
for the backend templates supported by Ultron.

These models will serve two purposes, they will be used to generate the
form on frontend, by giving the available options that can be configured.
They will also be used to generate the context for the template.
"""
from enum import Enum
from typing import Any, List, Union

from pydantic import BaseModel

from src.models.database_configs import (
    AvailableDatabases,
    MariaDBConfig,
    MySQLConfig,
    OracleConfig,
    PostgresConfig,
    SQLiteConfig,
)


# An enum of all available backend technologies, append to this enum when
# adding a new backend template.
class SupportedBackendTemplates(str, Enum):
    flask = "Flask"
    django = "Django"
    springboot = "Spring Boot"
    express = "Express"


SUPPORTED_DATABASES = {
    SupportedBackendTemplates.django: [
        AvailableDatabases.mysql,
        AvailableDatabases.mariadb,
        AvailableDatabases.sqlite,
        AvailableDatabases.oracle,
        AvailableDatabases.postgres,
    ],
    SupportedBackendTemplates.express: [
        AvailableDatabases.mysql,
        AvailableDatabases.mariadb,
        AvailableDatabases.sqlite,
        AvailableDatabases.postgres,
    ],
    SupportedBackendTemplates.flask: [
        AvailableDatabases.mysql,
        AvailableDatabases.sqlite,
        AvailableDatabases.postgres,
    ],
    SupportedBackendTemplates.springboot: [
        AvailableDatabases.mysql,
        AvailableDatabases.sqlite,
        AvailableDatabases.postgres,
    ],
}


class DjangoTemplate(BaseModel):
    _supported_databases = Union[
        PostgresConfig,
        MySQLConfig,
        MariaDBConfig,
        SQLiteConfig,
        OracleConfig,
    ]
    _db_fields = ["db_details"]
    template_url = "https://github.com/Ohuru-Tech/drf-cookiecutter"
    app_name: str
    project_name: str
    db_details: _supported_databases

    def get_template_configs(self):
        return {
            "template_url": self.template_url,
            "app_name": self.app_name,
            "project_name": self.project_name,
            "dev_db_url": self.db_details.get_db_url(),
            "prod_db_url": self.db_details.get_db_url(),
        }


class ExpressTemplate(BaseModel):
    _supported_databases = Union[
        PostgresConfig,
        MySQLConfig,
        MariaDBConfig,
        SQLiteConfig,
    ]
    _db_fields = ["db_details"]
    template_url = "https://github.com/Ohuru-Tech/express-cookiecutter"
    app_name: str
    project_name: str
    db_details: _supported_databases

    def get_template_configs(self):
        return {
            "template_url": self.template_url,
            "app_name": self.app_name,
            "project_name": self.project_name,
            "db_url": self.db_details.get_db_url(),
        }


TEMPLATE_CONFIGS = {
    SupportedBackendTemplates.django: DjangoTemplate,
    SupportedBackendTemplates.express: ExpressTemplate,
}
