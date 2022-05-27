from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from src.models.backend_templates import (
    SUPPORTED_DATABASES,
    TEMPLATE_CONFIGS,
    SupportedBackendTemplates,
)
from src.models.database_configs import (
    DATABASE_CONFIGS,
    AvailableDatabases,
)
from src.utils import BackendUtils

router = APIRouter()


@router.get("/backend/templates/")
def get_available_templates() -> List[str]:
    return list(SupportedBackendTemplates._member_map_.values())


@router.get("/backend/templates/{template_name}/")
def get_template_configs(
    template_name: SupportedBackendTemplates,
) -> dict:
    if template_name not in TEMPLATE_CONFIGS:
        raise HTTPException(
            status_code=404, detail="Template not found"
        )
    return list(TEMPLATE_CONFIGS[template_name].__annotations__.keys())


@router.get("/backend/templates/{template_name}/databases")
def get_supported_dbs(
    template_name: SupportedBackendTemplates,
) -> List[str]:
    return SUPPORTED_DATABASES.get(template_name, [])


@router.get("/backend/templates/databases/{db_type}")
def get_config_options_for_database(
    db_type: AvailableDatabases,
) -> List[str]:
    return list(
        DATABASE_CONFIGS.get(db_type, {}).__annotations__.keys()
    )


@router.post("/backend/templates/{template_name}/create")
async def generate_backend_template(
    template_name: SupportedBackendTemplates,
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

    # Parse the database model objects from dict and assign
    # them to the template
    for db_field in template_obj._db_fields:
        db_type = AvailableDatabases(
            settings.get(db_field, {}).get("db_type", None)
        )
        if db_type is None:
            raise HTTPException(
                status_code=400,
                detail={"db_type": "Database type is required"},
            )
        try:
            db_obj = DATABASE_CONFIGS.get(db_type).parse_obj(
                settings.get(db_field)
            )
            template_obj.__setattr__(db_field, db_obj)
        except ValidationError as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid settings: {e}"
            )

    # generate the template if everything is fine
    generated_dir = await BackendUtils.generate_backend_project(
        template_obj.template_url,
        template_obj.get_template_configs(),
    )

    return {"generated_dir": generated_dir}
