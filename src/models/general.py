from pydantic import BaseModel


class DownloadArgs(BaseModel):
    frontend_dir: str
    backend_dir: str
