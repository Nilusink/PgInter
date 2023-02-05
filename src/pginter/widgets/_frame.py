"""
_frame.py
04. February 2023

Frame - the base widget

Author:
Nilusink
"""
from ._geo_manager import GeometryManager
from ..theme import ThemeManager
from ..utils import arg_or_default
from ..types import *
import typing as tp
import pygame as pg


class DisplayConfig(tp.TypedDict):
    bg: Color
    ulr: int  # border radii
    urr: int
    llr: int
    lrr: int
    border_width: int
    border_color: Color


class Frame(GeometryManager):
    """
    The base widget
    """
    __parent: tp.Union["Frame", tp.Any]
    _display_config: BetterDict = ...
    _x: int = -1
    _y: int = -1

    def __init__(
            self,
            parent: tp.Union["Frame", tp.Any],
            width: int = ...,
            height: int = ...,
            bg_color: Color = ...,
            border_radius: int = ...,
            border_bottom_radius: int = ...,
            border_top_radius: int = ...,
            border_bottom_left_radius: int = ...,
            border_bottom_right_radius: int = ...,
            border_top_left_radius: int = ...,
            border_top_right_radius: int = ...,
            border_width: int = ...,
            border_color: Color = ...,
            margin: int = 0,
            padding: int = 0,
    ) -> None:
        """
        the most basic widget: a frame

        :param parent: the frames parent container
        :param width: width of the frame
        :param height: height of the frame
        :param bg_color: background color of the frame
        :param border_radius: border radius of the box (all four corners)
        :param border_width: how thick the border of the box should be
        :param border_color: the color of the border
        """

        # mutable defaults
        display_config: DisplayConfig = {
            "bg": Color(),
            "ulr": 0,
            "urr": 0,
            "llr": 0,
            "lrr": 0,
            "border_width": ...,
            "border_color": ...,
        }

        self._display_config = BetterDict(display_config)

        super().__init__(0, margin, padding)

        # arguments
        self.__parent = parent

        if width is not ...:
            self.width = width

        if height is not ...:
            self.height = height

        self._display_config["bg"] = self.__parent.theme.frame.bg if bg_color is ... else bg_color
        self._display_config["border_width"] = 0 if border_width is ... else border_width
        self._display_config["border_color"] = self.__parent.theme.frame.border if border_color is ... else border_color

        # border radii
        if border_radius is not ...:
            self._display_config["ulr"] = self._display_config["urr"] = border_radius
            self._display_config["llr"] = self._display_config["lrr"] = border_radius

        if border_top_radius is not ...:
            self._display_config["ulr"] = border_top_radius
            self._display_config["urr"] = border_top_radius

        if border_bottom_radius is not ...:
            self._display_config["llr"] = border_bottom_radius
            self._display_config["lrr"] = border_bottom_radius

        self._display_config.ulr = arg_or_default(border_top_left_radius, self._display_config.ulr, ...)
        self._display_config.urr = arg_or_default(border_top_right_radius, self._display_config.urr, ...)

        self._display_config.llr = arg_or_default(border_bottom_left_radius, self._display_config.llr, ...)
        self._display_config.lrl = arg_or_default(border_bottom_right_radius, self._display_config.lrr, ...)

    @property
    def theme(self) -> ThemeManager:
        return self.__parent.theme

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
        r_rect = pg.Rect((0, 0, self._width, self._height))
        pg.draw.rect(
            _surface,
            self._display_config.bg.rgba,
            r_rect,
            border_top_left_radius=self._display_config.ulr,
            border_top_right_radius=self._display_config.urr,
            border_bottom_left_radius=self._display_config.llr,
            border_bottom_right_radius=self._display_config.lrr,
        )

        if self._display_config.border_width > 0:
            pg.draw.rect(
                _surface,
                self._display_config.border_color.rgba,
                r_rect,
                width=self._display_config.border_width,
                border_top_left_radius=self._display_config.ulr,
                border_top_right_radius=self._display_config.urr,
                border_bottom_left_radius=self._display_config.llr,
                border_bottom_right_radius=self._display_config.lrr,
            )

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

        :param x: x-position
        :param y: y-position
        """
        if self.__parent.layout is not Absolute:
            raise TypeError("can't place in a container that is not managed by \"Absolute\"")

        self.__parent.add_child(self, x=x, y=y)

    def pack(
            self,
            anchor: tp.Literal["top", "bottom", "left", "right"] = TOP,
    ) -> None:
        """
        pack the frame in a parent container

        :param anchor: where to orient the frame at (direction)
        """
        if self.__parent.layout is not Pack:
            raise TypeError("can't pack in a container that is not managed by \"Pack\"")

        self.__parent.add_child(self, anchor=anchor.lower())

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
        self.width = width
        self.height = height

    def delete(self) -> None:
        """
        delete the widget
        """
        self.__parent = ...

        # terminate all children
        for child in self._children:
            child.delete()
