"""
_frame.py
04. February 2023

Frame - the base widget

Author:
Nilusink
"""
from ._geo_manager import GeometryManager
from .._pg_root import PgRoot
from ..types import Color
import typing as tp


class Frame(GeometryManager):
    """
    The base widget
    """
    _bg: Color = ...
    _width: float = -1   # -1 means not configured -> takes minimum size required by its children
    _height: float = -1  # or the size it gets by the parents geometry manager
    __parent: tp.Union["Frame", PgRoot]

    def __init__(
            self,
            parent: tp.Union["Frame", PgRoot],
            width: int = ...,
            height: int = ...,
            bg_color: Color = ...
    ) -> None:
        super().__init__()

        # arguments
        self.__parent = parent

        if width is not ...:
            self._width = width

        if height is not ...:
            self._height = height

        self._bg = self.__parent.theme.frame.bg if bg_color is ... else bg_color

    def get_size(self) -> tuple[int, int]:
        """
        get the frames size (including children)
        """
        # width
        width = self._width
        if width == -1:
            ...

        # height
        height = self._height
        if height == -1:
            ...

        return width.__floor__(), height.__floor__()

    def draw(self) -> None:
        """
        draw the frame
        """
