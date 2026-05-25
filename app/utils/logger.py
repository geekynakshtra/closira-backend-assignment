import json
import logging

logger = logging.getLogger("closira")

logger.setLevel(logging.INFO)

handler = logging.StreamHandler()

formatter = logging.Formatter("%(message)s")

handler.setFormatter(formatter)

logger.addHandler(handler)


def log_event(event: dict):
    logger.info(json.dumps(event))
