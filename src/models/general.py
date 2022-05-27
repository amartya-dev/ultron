from pydantic import BaseModel


class DownloadArgs(BaseModel):
    project_name: str
    frontend_dir: str
    backend_dir: str
