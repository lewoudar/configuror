"""Module which holds the Config class"""
import os
from importlib import import_module
from typing import Dict, List, Optional, TypeVar

Object = TypeVar('Object')


class Config(dict):

    def __init__(self, mapping_files: Dict[str, List[str]] = None, files: List[str] = None, **kwargs):
        super(Config, self).__init__(**kwargs)
    
    def _check_path(self, filename: str):
        pass

    @staticmethod
    def getenv(key: str) -> Optional[str]:
        return os.getenv(key)

    def load_from_object(self, obj: Object) -> None:
        if isinstance(obj, str):
            obj = import_module(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
