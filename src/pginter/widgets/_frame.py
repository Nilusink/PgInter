"""
_frame.py
04. February 2023

Frame - the base widget

Author:
Nilusink
"""
from ._geo_manager import GeometryManager
from ..types import Color, BetterDict
import typing as tp
import pygame as pg


class DisplayConfig(tp.TypedDict):
    bg: Color
    ulr: int  # border radii
    urr: int
    llr: int
    lrr: int


class Frame(GeometryManager):
    """
    The base widget
    """
    __parent: tp.Union["Frame", tp.Any]
    _display_config: BetterDict[DisplayConfig] = ...
    _x: int = -1
    _y: int = -1

    def __init__(
            self,
            parent: tp.Union["Frame", tp.Any],
            width: int = ...,
            height: int = ...,
            bg_color: Color = ...,
            border_radius: int = ...,
    ) -> None:
        # mutable defaults
        self._display_config = BetterDict({
            "bg": Color(),
            "ulr": 0,
            "urr": 0,
            "llr": 0,
            "lrr": 0
        })

        super().__init__()

        # arguments
        self.__parent = parent

        if width is not ...:
            self._width = width

        if height is not ...:
            self._height = height

        self._display_config["bg"] = self.__parent.theme.frame.bg if bg_color is ... else bg_color

        if border_radius:
            self._display_config["ulr"] = self._display_config["urr"] = border_radius
            self._display_config["llr"] = self._display_config["lrr"] = border_radius

    def get_size(self) -> tuple[int, int]:
        """
        get the frames size (including children)
        """
        calculated_size = self.calculate_size()

        # width
        width = self._width
        if width == -1:
            width = calculated_size[0]
            width = 0 if width == -1 else width

        # height
        height = self._height
        if height == -1:
            height = calculated_size[1]
            height = 0 if height == -1 else height

        return width.__floor__(), height.__floor__()

    def draw(self, surface: pg.Surface) -> None:
        """
        draw the frame
        """
        width, height = self.get_size()
        _surface = pg.Surface((width, height), pg.SRCALPHA)

        # draw the frame
        pg.draw.rect(_surface, self._display_config.bg.rgba, pg.Rect((0, 0, self._width, self._height)))

        # draw children
        for child, params in self._child_params:
            child.draw(_surface)

        # draw
        surface.blit(_surface, (self._x, self._y))

    def place(
            self,
            x: int,
            y: int,
    ) -> None:
        """
        place the frame in a parent container
        """
        self.__parent.add_child(self, x=x, y=y)

    def set_position(self, x: int, y: int) -> None:
        """
        set the child's position (used by parents)
        """
        self._x = x
        self._y = y

    def set_size(self, width: float, height: float) -> None:
        """
        set the child's size (used by parens)
        """
        self._width = width
        self._height = height
