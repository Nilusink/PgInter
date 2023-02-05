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


def display_configurify(key: str) -> str:
    """
    convert a Frame init key to it's corresponding DisplayConfig key
    """
    replaces = [
        ("bg_color", "bg"),
        ("border_bottom_left_radius", "blr"),
        ("border_bottom_right_radius", "brr"),
        ("border_top_left_radius", "ulr"),
        ("border_top_right_radius", "urr"),
    ]

    for init, config in replaces:
        if key == init:
            return config

    return key


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
            layout: int = 0,
            border_radius: int = ...,
            border_bottom_radius: int = ...,
            border_top_radius: int = ...,
            border_bottom_left_radius: int = ...,
            border_bottom_right_radius: int = ...,
            border_top_left_radius: int = ...,
            border_top_right_radius: int = ...,
            border_width: int = ...,
            border_color: Color = ...,
            margin: int = ...,
            padding: int = ...,
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

        self.__parent = parent

        # mutable defaults
        display_config: DisplayConfig = {
            "bg": ...,
            "ulr": self.theme.frame.border_top_left_radius if "border_top_left_radius" in self.theme.frame else 0,
            "urr": self.theme.frame.border_top_right_radius if "border_top_right_radius" in self.theme.frame else 0,
            "llr": self.theme.frame.border_bottom_left_radius if "border_bottom_left_radius" in self.theme.frame else 0,
            "lrr": self.theme.frame.border_bottom_right_radius if "border_bottom_right_radius" in self.theme.frame else 0,
            "border_width": self.theme.frame.border_width if "border_width" in self.theme.frame else 0,
            "border_color": ...,
        }

        self._display_config = BetterDict(display_config)

        if margin is ...:
            margin = self.theme.frame.margin if "margin" in self.theme.frame else 0

        if padding is ...:
            padding = self.theme.frame.padding if "padding" in self.theme.frame else 0

        super().__init__(layout, margin, padding)

        # arguments
        if width is not ...:
            self.width = width

        if height is not ...:
            self.height = height

        self._display_config["bg"] = self.theme.frame.bg if bg_color is ... else bg_color
        if border_width is not ...:
            self._display_config["border_width"] = border_width

        self._display_config["border_color"] = self.theme.frame.border if border_color is ... else border_color

        # border radii
        if border_radius is ... and "border_radius" in self.theme.frame:
            border_radius = self.theme.frame.border_radius

        if border_bottom_radius is ... and "border_bottom_radius" in self.theme.frame:
            border_bottom_radius = self.theme.frame.border_bottom_radius

        if border_top_radius is ... and "border_top_radius" in self.theme.frame:
            border_top_radius = self.theme.frame.border_top_radius

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

    def configure(self, **kwargs) -> None:
        """
        configure any of the init parameters (except parent)
        """
        for key, value in kwargs.items():
            match key:
                case "width":
                    self.width = value

                case "height":
                    self.height = value

                case "border_radius":
                    self._display_config.ulr = value
                    self._display_config.urr = value
                    self._display_config.blr = value
                    self._display_config.brr = value

                case "border_bottom_radius":
                    self._display_config.blr = value
                    self._display_config.brr = value

                case "border_top_radius":
                    self._display_config.ulr = value
                    self._display_config.urr = value

                case _:
                    # check if in display config
                    new_key = display_configurify(key)

                    if new_key in self._display_config:
                        if isinstance(value, type(self._display_config[new_key])):
                            raise TypeError(
                                f"Can't change \"{self._display_config[new_key]}\" to \"{value}\": "
                                f"invalid type!"
                            )

                        self._display_config[key] = value

                    elif key in self.layout_params:
                        if isinstance(value, type(self.layout_params[new_key])):
                            raise TypeError(
                                f"Can't change \"{self.layout_params[new_key]}\" to \"{value}\": "
                                f"invalid type!"
                            )

                        self.layout_params[key] = value

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
        pack the frame into a parent container

        :param anchor: where to orient the frame at (direction)
        """
        if self.__parent.layout is not Pack:
            raise TypeError("can't pack in a container that is not managed by \"Pack\"")

        self.__parent.add_child(self, anchor=anchor.lower())

    def grid(
            self,
            row: int,
            column: int,
            sticky: str = "",
    ) -> None:
        """
        grid the frame into a parent container

        :param row: the row the item should be placed in
        :param column: the column the item should be placed in
        :param sticky: expansion, can be a combination of "n", "e", "s", "w"
        """
        if self.__parent.layout is not Grid:
            raise TypeError("can't grid in a container that is not managed by \"Grid\"")

        self.__parent.add_child(self, row=row, column=column, sticky=sticky)

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
