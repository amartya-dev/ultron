import logging
from cgitb import handler

from src.config import app_config

log = logging.getLogger(__name__)
log.setLevel(app_config.log_level)
log.propagate = False

handler = logging.StreamHandler()
handler.setLevel(app_config.log_level)

formatter = logging.Formatter("%(levelname)s: %(asctime)s %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)
