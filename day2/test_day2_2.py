# test_exercise.py

import pytest
import json
from exercise import load_config, validate_config


# 1. Use tmp_path to create a config.json and verify load_config reads it
def test_load_config_reads_file(tmp_path):
    # TODO: create a JSON file in tmp_path, call load_config, assert values
    pass


# 2. Use tmp_path + monkeypatch to verify ENV vars override the file values
def test_env_overrides(tmp_path, monkeypatch):
    # TODO: create a config file, set APP_PORT and APP_DEBUG env vars, assert overrides
    pass


# 3. Use parametrize to test validate_config with at least 4 different configs
# Hint: @pytest.mark.parametrize("config, expected_errors", [...])
def test_validate_config():
    # TODO: test valid config, invalid port, missing host, bad debug type
    pass