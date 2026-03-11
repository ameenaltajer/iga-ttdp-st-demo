# ── exercise.py ──────────────────────────────────────────────

import os
import json

def load_config(filepath):
    """Load a JSON config file and apply environment overrides."""
    with open(filepath, "r") as f:
        config = json.load(f)

    # ENV vars override file values
    if os.environ.get("APP_PORT"):
        config["port"] = int(os.environ["APP_PORT"])
    if os.environ.get("APP_DEBUG"):
        config["debug"] = os.environ["APP_DEBUG"].lower() == "true"

    return config


def validate_config(config):
    """Return a list of error strings. Empty list means valid."""
    errors = []
    if not isinstance(config.get("port"), int) or not (1 <= config["port"] <= 65535):
        errors.append("invalid port")
    if "host" not in config or not config["host"]:
        errors.append("missing host")
    if not isinstance(config.get("debug"), bool):
        errors.append("debug must be bool")
    return errors