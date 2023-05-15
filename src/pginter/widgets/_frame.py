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
    _focused: bool = False
    style: Style = ...
    hover_style: Style = ...
    active_style: Style = ...
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
        self.style = style if style is not ... else Style()
        self.active_style = active_style if active_style is not ... else Style()
        self.hover_style = hover_style if hover_style is not ... else Style()

        # TODO: implement styles
        if min_width is not ...:
            self._width = min_width

        if min_height is not ...:
            self._height = min_height

        self.__parent = parent

        self.__parent.theme.notify_on(ThemeManager.NotifyEvent.theme_reload, self.notify)

        # mutable defaults
        self.style.backgroundColor = ...

        # load boarder radii from default theme
        self.style.borderTopLeftRadius = 0
        self.style.borderTopRightRadius = 0
        self.style.borderBottomLeftRadius = 0
        self.style.borderBottomRightRadius = 0

        if "border_top_left_radius" in self.theme.frame:
            self.style.borderTopLeftRadius = self.theme.frame.border_top_left_radius

        if "border_top_right_radius" in self.theme.frame:
            self.style.borderTopRightRadius = self.theme.frame.border_top_right_rasdius

        if "border_bottom_left_radius" in self.theme.frame:
            self.style.borderBottomLeftRadius = self.theme.frame.border_bottom_left_radius

        if "border_bottom_right_radius" in self.theme.frame:
            self.style.borderBottomRightRadius = self.theme.border_bottom_right_radius

        # border config
        self.style.borderWidth = 0
        self.style.borderColor = Color.from_rgb(255, 0, 0)

        if "border_width" in self.theme.frame:
            self.style.borderWidth = self.theme.frame.border_width

        if "border" in self.theme.frame:
            self.style.borderColor = self.theme.frame.border

        if margin is ...:
            margin = self.theme.frame.margin if "margin" in self.theme.frame else 0

        if padding is ...:
            padding = self.theme.frame.padding if "padding" in self.theme.frame else 0

        super().__init__(layout, margin, padding)

        self.style.notify_on("margin", self.notify)
        self.style.notify_on("padding", self.notify)

        # arguments
        if width is not ...:
            self.style.width = width

        if height is not ...:
            self.style.height = height

        self.style.backgroundColor = self.theme.frame.bg1 if bg is ... else bg
        if isinstance(self.__parent, Frame) and \
                self.__parent.style.backgroundColor == self.theme.frame.bg1:
            self.style.backgroundColor = self.theme.frame.bg2 if bg is ... else bg

        if border_width is not ...:
            self.style.borderWidth = border_width

        self.style.borderColor = self.theme.frame.border if border_color is ... else border_color

        # border radii
        if border_radius is ... and "border_radius" in self.theme.frame:
            border_radius = self.theme.frame.border_radius

        if border_bottom_radius is ... and "border_bottom_radius" in self.theme.frame:
            border_bottom_radius = self.theme.frame.border_bottom_radius

        if border_top_radius is ... and "border_top_radius" in self.theme.frame:
            border_top_radius = self.theme.frame.border_top_radius

        self.style.borderTopLeftRadius = border_radius
        self.style.borderTopRightRadius = border_radius
        self.style.borderBottomLeftRadius = border_radius
        self.style.borderBottomRightRadius = border_radius

        if border_top_radius is not ...:
            self.style.borderTopLeftRadius = border_top_radius
            self.style.borderTopRightRadius = border_top_radius

        if border_bottom_radius is not ...:
            self.style.borderBottomLeftRadius = border_bottom_radius
            self.style.borderBottomRightRadius = border_bottom_radius

        self.style.borderTopLeftRadius = arg_or_default(
            border_top_left_radius,
            self.style.borderTopLeftRadius,
            ...
        )
        self.style.borderTopRightRadius = arg_or_default(
            border_top_right_radius,
            self.style.borderTopRightRadius,
            ...
        )

        self.style.borderBottomLeftRadius = arg_or_default(
            border_bottom_left_radius,
            self.style.borderBottomLeftRadius,
            ...
        )
        self.style.borderBottomRightRadius = arg_or_default(
            border_bottom_right_radius,
            self.style.borderBottomRightRadius,
            ...
        )

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
                    self.style.borderRadius = value

                case "border_bottom_radius":
                    self.style.borderBottomRadius = value

                case "border_top_radius":
                    self.style.borderTopRadius = value

                case _:
                    # check if in display config
                    new_key = display_configurify(key)

                    if new_key in self.style:
                        if isinstance(value, type(self.style[new_key])):
                            raise TypeError(
                                f"Can't change \"{self.style[new_key]}\" to \"{value}\": "
                                f"invalid type!"
                            )

                        self.style[key] = value

                    elif key in self.layout_params:
                        if isinstance(value, type(self.style[new_key])):
                            raise TypeError(
                                f"Can't change \"{self.layout_params[new_key]}\" to \"{value}\": "
                                f"invalid type!"
                            )

                        self.layout_params[key] = value

    # interfacing
    def notify(
            self,
            event: ThemeManager.NotifyEvent | Style.NotifyEvent,
            info: tp.Any = ...
    ) -> None:
        """
        gets called by another class
        """
        match event:
            case ThemeManager.NotifyEvent.theme_reload:
                print("theme changed")
                # the theme has been reloaded
                # if not self._display_config_configured.bg:
                #     if isinstance(self.__parent, Frame) and self.__parent._display_config["bg"] == self.theme.frame.bg1:
                #         self._display_config.bg = self.theme.frame.bg2
                #
                #     else:
                #         self._display_config.bg = self.theme.frame.bg1
                #
                # if not self._display_config_configured.border_color:
                #     self._display_config.border_color = self.theme.frame.border
                #
                # if not self._display_config_configured.border_radius:
                #     self._display_config.border_radius = self.theme.frame.border_radius

            case Style.NotifyEvent.property_change:
                print(f"style changed: {info}, new value: {self.style[info]}")

                if info in ("padding", "margin"):
                    self.layout_params[info] = self.style[info]

            case _:
                super().notify(event, info)

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

    def get_position(self) -> tuple[int, int]:
        return self._x, self._y

    def draw(self, surface: pg.Surface) -> None:
        """
        draw the frame
        """
        current_style = self.style

        if self._is_hover:
            current_style = self.style.overwrite(self.hover_style)

        if self._is_active:
            current_style = self.style.overwrite(self.hover_style).overwrite(
                self.active_style
            )

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
            current_style.backgroundColor.irgba,
            r_rect,
            border_top_left_radius=current_style.borderTopLeftRadius,
            border_top_right_radius=current_style.borderTopRightRadius,
            border_bottom_left_radius=current_style.borderBottomLeftRadius,
            border_bottom_right_radius=current_style.borderBottomRightRadius
        )

        if current_style.borderWidth > 0:
            pg.draw.rect(
                _surface,
                current_style.borderColor.irgba,
                r_rect,
                width=current_style.borderWidth,
                border_top_left_radius=current_style.borderTopLeftRadius,
                border_top_right_radius=current_style.borderTopRightRadius,
                border_bottom_left_radius=current_style.borderBottomLeftRadius,
                border_bottom_right_radius=current_style.borderBottomRightRadius
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
