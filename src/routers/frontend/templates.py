from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from src.models.frontend_templates import (
    TEMPLATE_CONFIGS,
    SupportedFrontendTemplates,
)
from src.utils import FrontendUtils

router = APIRouter()


@router.get("/frontend/templates/")
def get_available_templates() -> List[str]:
    return list(SupportedFrontendTemplates._member_map_.values())


@router.get("/frontend/templates/{template_name}/")
def get_template_configs(
    template_name: SupportedFrontendTemplates,
) -> dict:
    if template_name not in TEMPLATE_CONFIGS:
        raise HTTPException(
            status_code=404, detail="Template not found"
        )
    return list(TEMPLATE_CONFIGS[template_name].__annotations__.keys())


@router.post("/frontend/templates/{template_name}/create")
async def generate_frontend_template(
    template_name: SupportedFrontendTemplates,
    settings: dict,
):
    # Try constructing the template class from dict
    template_class = TEMPLATE_CONFIGS.get(template_name)

    if template_class is None:
        raise HTTPException(
            status_code=404, detail="Template not found"
        )

    # Parse the template model object from dict
    try:
        template_obj = template_class.parse_obj(settings)
    except ValidationError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid settings: {e}"
        )

    # generate the template if everything is fine
    generated_dir = await FrontendUtils.generate_frontend_project(
        template_obj.template_url,
        template_obj.get_template_configs(),
    )

    return {"generated_dir": generated_dir}
