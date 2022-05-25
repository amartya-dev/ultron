import os

import yaml
from cookiecutter.main import cookiecutter
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Template(BaseModel):
    url: str


class CookieCutterSettings(BaseModel):
    github_repository_name: str
    app_name: str
    email: str
    description: str
    github_username: str


@app.post("/clone_via_cookiecutter")
def clone_via_cookiecutter(template: Template, settings: CookieCutterSettings):
    cookiecutter(template.url, extra_context=settings.dict(), no_input=True)
    return {"template": template, "settings": settings}
