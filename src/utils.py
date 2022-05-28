import os
import pathlib
import shutil

from cookiecutter.main import cookiecutter

TEMPS_DIR = os.path.join(
    pathlib.Path(__file__).parent.resolve(), "..", "temps"
)


def create_next_available_folder(type: str) -> str:
    """
    This function will create a folder in the temp folder
    with the name of the type and return the path of that
    folder.
    """
    os.makedirs(TEMPS_DIR, exist_ok=True)
    os.chdir(TEMPS_DIR)
    temp_num = 1

    while os.path.exists(f"{type}{temp_num}"):
        temp_num += 1

    os.mkdir(f"{type}{temp_num}")
    return os.path.join(TEMPS_DIR, f"{type}{temp_num}")


def slugify(string: str) -> str:
    """
    This function will slugify the string.
    """
    return (
        string.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "_")
        .strip()
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
        backend_dir = create_next_available_folder("backend")
        os.chdir(backend_dir)

        cookiecutter(
            template_url, extra_context=project_configs, no_input=True
        )

        return str(
            os.path.join(
                backend_dir,
                slugify(project_configs.get("project_name")),
            )
        )


class FrontendUtils:
    """
    These will be used for actually creating the folders and then later
    cloning them and stuff
    """

    @staticmethod
    async def generate_frontend_project(
        template_url: str, project_configs: dict
    ):
        frontend_dir = create_next_available_folder("frontend")
        os.chdir(frontend_dir)

        cookiecutter(
            template_url, extra_context=project_configs, no_input=True
        )

        return str(
            os.path.join(
                frontend_dir,
                slugify(project_configs.get("project_name")),
            )
        )


class GeneralUtils:
    """
    These are not associated with either backend or frontend, pretty much independent
    """

    @staticmethod
    async def generate_zip(frontend_dir: str, backend_dir: str):
        # Create a project folder in the temp dir
        project_folder = create_next_available_folder("project")
        os.chdir(TEMPS_DIR)
        shutil.copytree(
            backend_dir,
            os.path.join(project_folder, backend_dir.split("/")[-1]),
        )
        shutil.copytree(
            frontend_dir,
            os.path.join(project_folder, frontend_dir.split("/")[-1]),
        )
        shutil.make_archive(
            project_folder.split("/")[-1], "zip", project_folder
        )

        shutil.rmtree("/".join(frontend_dir.split("/")[:-1]))
        shutil.rmtree("/".join(backend_dir.split("/")[:-1]))

        return os.path.join(
            TEMPS_DIR, f"{project_folder.split('/')[-1]}.zip"
        )
