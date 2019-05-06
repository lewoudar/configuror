"""Helper functions for the project"""
from configparser import ConfigParser


def convert_ini_config_to_dict(config: ConfigParser) -> dict:
    """Translates a configparser object into a dict."""
    return {key: dict(value) for key, value in config.items()}
