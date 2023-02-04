"""
_manager.py
04. February 2023

The built-in theme manager

Author:
Nilusink
"""
from ..types import *
import typing as tp
import json


DEFAULT_THEME: str = "themes/default.json"


class ThemeManager:
    """
    the build-in theme manager
    """
    _config: dict[str, str | dict] = ...
    instance = ...

    def __new__(cls, *args, **kwargs):
        """
        only on instance of a theme manager should ever exist
        """
        if cls.instance is ...:
            cls.instance = super().__new__(cls, *args, **kwargs)

        return cls.instance

    def __init__(self, theme_path: str = ...) -> None:
        self._config = json.load(open(DEFAULT_THEME if theme_path is ... else theme_path, "r"))

        for key in self._config.copy():
            for ckey, color in self._config[key].items():
                if isinstance(color, str):
                    self._config[key][ckey] = Color.from_hex(color, 255)

                elif isinstance(color, tp.Iterable) and isinstance(color[0], float) or isinstance(color[0], int):
                    self._config[key][ckey] = Color.from_rgb(*color)

    def __getattr__(self, item: str) -> str | BetterDict:
        """
        for better accessibility
        """
        val = self._config[item]

        if isinstance(val, dict):
            return BetterDict(val)

        elif isinstance(val, str):
            return val

        else:
            raise ValueError(f"Invalid type for key \"{item}\": {type(val)}")

    def __getitem__(self, item: str) -> str | BetterDict:
        return self.__getattr__(item)

