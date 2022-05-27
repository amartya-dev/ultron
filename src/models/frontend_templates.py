"""
This file will be used to store the backend tempalte config structures required 
for the frontend templates supported by Ultron.

These models will serve two purposes, they will be used to generate the
form on frontend, by giving the available options that can be configured.
They will also be used to generate the context for the template.
"""
from enum import Enum

from pydantic import BaseModel


class SupportedFrontendTemplates(str, Enum):
    react = "React"
    flutter = "Flutter"


class ReactTemplate(BaseModel):
    template_url = "https://github.com/Ohuru-Tech/react-cookiecutter"
    app_name: str
    project_name: str

    def get_template_configs(self):
        return {
            "app_name": self.app_name,
            "project_name": self.project_name,
        }


TEMPLATE_CONFIGS = {
    SupportedFrontendTemplates.react: ReactTemplate,
}
