import importlib
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.config import app_config
from src.logger import log

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

log.info("Loading routes ...")

# This will automatically scan for new routers and load them
current_dir = os.getcwd()
for sub_dir, dirs, files in os.walk(
    os.path.join(current_dir, "src/routers")
):
    for file in files:
        if file.endswith(".py"):
            log.info(f"Loading {file} ...")
            full_path = (
                os.path.join(sub_dir, file)
                .replace(".py", "")
                .replace(current_dir, "")
                .replace("/", ".")
            )[1:]
            module = importlib.import_module(full_path)
            app.include_router(module.router)
