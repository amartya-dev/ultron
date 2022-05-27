from typing import List

from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.models.general import DownloadArgs
from src.utils import GeneralUtils

router = APIRouter()


@router.post("/download/")
async def download_generated_project(
    args: DownloadArgs,
) -> FileResponse:
    file_location = await GeneralUtils.generate_zip(
        frontend_dir=args.frontend_dir,
        backend_dir=args.backend_dir,
        project_name=args.project_name,
    )
    return FileResponse(file_location, media_type="application/zip")
