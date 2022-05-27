import os
import pathlib

from cookiecutter.main import cookiecutter

TEMPS_DIR = os.path.join(
    pathlib.Path(__file__).parent.resolve(), "..", "temps"
)


class BackendUtils:
    """
    These will be used for actually creating the folders and then later
    cloning them and stuff
    """

    @staticmethod
    async def generate_backend_project(
        template_url: str, project_configs: dict
    ):
        print(TEMPS_DIR)
        os.makedirs(TEMPS_DIR, exist_ok=True)
        os.chdir(TEMPS_DIR)
        temp_num = 1

        while os.path.exists(f"backend{temp_num}"):
            temp_num += 1

        os.mkdir(f"backend{temp_num}")
        os.chdir(f"backend{temp_num}")

        cookiecutter(
            template_url, extra_context=project_configs, no_input=True
        )

        return os.path.join(TEMPS_DIR, f"backend{temp_num}")
