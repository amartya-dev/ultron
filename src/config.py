import ast
import configparser
import logging
import os

log = logging.getLogger(__name__)


class Config:
    """
    Allows for providing a centralised configuration for Ultron/.
    Typical use will look something like this:

    from src.config import app_config
    my_log_level = app_config.log_level

    While it is possible to call ``get_config_value()`` directly,
    it is recommended that the new configurations should be added
    as ``@property`` to the ``Config`` class.
    """

    _config = None

    def __init__(self):
        self.read_config_files()

    def config_files(self):
        """
        Returns a list of config files to be read.
        Included as a future proof method to allow for adding
        different settings for different envs.
        """
        return ["ultron.conf"]

    def config_paths(self):
        """
        Returns a list of paths to config files to be read.
        """
        api_root = os.getcwd()
        config_files = self.config_files()
        return [
            os.path.join(api_root, config_file)
            for config_file in config_files
        ]

    def read_config_files(self):
        """
        Loads the configuration values into self._config
        """

        self._config = configparser.ConfigParser()
        config_paths = self.config_paths()

        if config_paths:
            self._config.read(config_paths)

    def get_config_value(
        self, section, key, default=None, required=False
    ):
        """
        Returns the value of the config key.

        :param section: The section of the config file to look in.
        :param ke: The key to look for.
        :param default: The default value to return if the key is not found.
        :param required: If the key is required or not.

        This function takes into account the environment variables as well.
        The env variables will actually be given preference, the format that
        should be used to set the environment variables is something like
        `FOO_BAR_BAZ`, where foo is the section and bar_baz is the key
        """

        # Check first for the environment variable
        env_key = f"{section.upper()}_{key.upper()}"
        val = os.environ.get(env_key)

        if val is not None:
            return val

        # Check for the config file
        val = self._config.get(section, key, fallback=default)

        if val is None:
            message = f"Missing config value: {section}.{key}"
            if required:
                raise KeyError(message)
            log.warning(message)

        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return val

    @property
    def log_level(self):
        """
        Retrieve the log level config value
        """
        return self.get_config_value("logging", "level", default="INFO")

    @property
    def allowed_origins(self):
        """
        Retrieve the allowed origins config value
        """
        return self.get_config_value(
            "cors", "allowed_origins", default='["*"]'
        )


app_config = Config()
