"""Module which holds the Config class"""
import os
from typing import Dict, List, Optional


class Config(dict):

    def __init__(self, mapping_files: Dict[str, List[str]] = None, files: List[str] = None, **kwargs):
        super(Config, self).__init__(**kwargs)

    @staticmethod
    def getenv(key: str) -> Optional[str]:
        return os.getenv(key)
