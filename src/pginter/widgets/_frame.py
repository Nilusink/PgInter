"""
_frame.py
04. February 2023

Frame - the base widget

Author:
Nilusink
"""
from ._geo_manager import GeometryManager
from ..utils import arg_or_default
from ..theme import ThemeManager
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


class DisplayConfigConfigured(tp.TypedDict):
    bg: bool
    ulr: bool
    urr: bool
    llr: bool
    lrr: bool
    border_width: bool
    border_color: bool


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
    __parent: tp.Union["Frame", tp.Any] = ...
    _display_config: BetterDict = ...
    _display_config_configured: BetterDict = ...
    _focused: bool = False
    _style: Style = ...
    _hover_style: Style = ...
    _active_style: Style = ...
    _x: int = -1
    _y: int = -1

    def __init__(
            self,
            parent: tp.Union["Frame", tp.Any],
            width: int = ...,
            height: int = ...,
            bg: Color = ...,
            layout: Layout = 0,
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
            min_width: int = ...,
            min_height: int = ...,
            style: Style = ...,
            active_style: Style = ...,
            hover_style: Style = ...
    ) -> None:
        """
        The most basic widget: a frame.
        When using the  style  property, all other styles will be overwritten!

        :param parent: the frames parent container
        :param width: width of the frame
        :param height: height of the frame
        :param bg: background color of the frame
        :param border_radius: border radius of the box (all four corners)
        :param border_width: how thick the border of the box should be
        :param border_color: the color of the border
        """
        self._style = style if style is not ... else Style()
        self._active_style = active_style if active_style is not ... else Style()
        self._hover_style = hover_style if hover_style is not ... else Style()

        # TODO: implement styles
        if min_width is not ...:
            self._width = min_width

        if min_height is not ...:
            self._height = min_height

        self.__parent = parent

        self.__parent.theme.notify_on(ThemeManager.NotifyEvent.theme_reload, self.notify)

        # mutable defaults
        display_config: DisplayConfig = {
            "bg": ...,
            "ulr": self.theme.frame.border_top_left_radius if "border_top_left_radius" in self.theme.frame else 0,
            "urr": self.theme.frame.border_top_right_radius if "border_top_right_radius" in self.theme.frame else 0,
            "llr": self.theme.frame.border_bottom_left_radius if "border_bottom_left_radius" in self.theme.frame else 0,
            "lrr": self.theme.frame.border_bottom_right_radius if "border_bottom_right_radius" in self.theme.frame else 0,
            "border_width": self.theme.frame.border_width if "border_width" in self.theme.frame else 0,
            "border_color": self.theme.frame.border if "border" in self.theme.frame else Color.from_rgb(255, 0, 0),
        }

        display_config_configured: DisplayConfigConfigured = {
            "bg": bg is not ...,
            "ulr": border_radius is not ... or border_top_radius is not ... or border_top_left_radius is not ...,
            "urr": border_radius is not ... or border_top_radius is not ... or border_top_right_radius is not ...,
            "llr": border_radius is not ... or border_bottom_radius is not ... or border_bottom_left_radius is not ...,
            "lrr": border_radius is not ... or border_bottom_radius is not ... or border_bottom_right_radius is not ...,
            "border_width": border_width is not ...,
            "border_color": border_color is not ...,
        }

        self._display_config = BetterDict(display_config)
        self._display_config_configured = BetterDict(display_config_configured)

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

        self._display_config["bg"] = self.theme.frame.bg1 if bg is ... else bg
        if isinstance(self.__parent, Frame) and self.__parent._display_config["bg"] == self.theme.frame.bg1:
            self._display_config["bg"] = self.theme.frame.bg2 if bg is ... else bg

        print(f"set background: ", self._display_config.bg, bg)

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

    @property
    def parent(self) -> tp.Union["Frame", tp.Any]:
        return self.__parent

    def set_focus(self):
        """
        set this item as currently focused
        """
        self.parent.notify_focus(self)
        self._focused = True

    def stop_focus(self):
        """
        remove focus from this item
        """
        self.parent.notify_focus()
        self._focused = False

    def notify_focus(self, widget: tp.Union["GeometryManager", None] = None):
        """
        notify the root that a widget has been set as focus
        """
        self.parent.notify_focus(widget)

    def _on_focus(self) -> None:
        """
        called when button is clicked
        """

    def _on_hover(self) -> None:
        """
        called on hover
        """

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

                case "min_width":
                    self._width = value

                case "min_height":
                    self._height = value

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

    # interfacing
    def notify(self, event: ThemeManager.NotifyEvent) -> None:
        """
        gets called by another class
        """
        match event:
            case ThemeManager.NotifyEvent.theme_reload:
                # the theme has been reloaded
                if not self._display_config_configured.bg:
                    if isinstance(self.__parent, Frame) and self.__parent._display_config["bg"] == self.theme.frame.bg1:
                        self._display_config.bg = self.theme.frame.bg2

                    else:
                        self._display_config.bg = self.theme.frame.bg1

                if not self._display_config_configured.border_color:
                    self._display_config.border_color = self.theme.frame.border

                if not self._display_config_configured.border_radius:
                    self._display_config.border_radius = self.theme.frame.border_radius

    def get_size(self) -> tuple[int, int]:
        """
        get the frames size (including children)
        """
        # print(f"getting frame size: {self.width, self.height}")

        # width
        width = self._width if self._width_configured else \
            self.assigned_width

        # height
        height = self._height if self._height_configured else \
            self.assigned_height

        return width.__floor__(), height.__floor__()

    def draw(self, surface: pg.Surface) -> None:
        """
        draw the frame
        """
        width, height = self.get_size()

        # print(f"frame size: {width, height=}, "
        #       f"{self.assigned_width, self.assigned_height=}, "
        #       f"{self._width_configured, self._height_configured=}")

        # print(f"drawing: \"{type(self).__name__}\"", (width, height), self._x, self._y, self._display_config.bg)
        _surface = pg.Surface((width, height), pg.SRCALPHA)

        # draw the frame
        r_rect = pg.Rect((0, 0, width, height))
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
        if self.__parent.layout is not Layout.Absolute:
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
        if self.__parent.layout is not Layout.Pack:
            raise TypeError(
                "can't pack in a container that is not managed by \"Pack\"."
                f" Configured Manager: {self.__parent.layout}"
            )

        self.__parent.add_child(self, anchor=anchor.lower())

    def grid(
            self,
            row: int,
            column: int,
            sticky: str = "",
            margin: int = 0,
    ) -> None:
        """
        grid the frame into a parent container

        :param row: the row the item should be placed in
        :param column: the column the item should be placed in
        :param sticky: expansion, can be a combination of "n", "e", "s", "w"
        :param margin: the distance to the grids borders
        """
        if self.__parent.layout is not Layout.Grid:
            raise TypeError("can't grid in a container that is not managed by \"Grid\"")

        self.__parent.add_child(self, row=row, column=column, sticky=sticky, margin=margin)

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
