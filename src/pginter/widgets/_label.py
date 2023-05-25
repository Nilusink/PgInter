"""
_label.py
10. February 2023

A thing to display text

Author:
Nilusink
"""
from ..types import Color, Layout, Style, Variable, StringVar, GeoNotes
from ..utils import arg_or_default
from ..theme import ThemeManager
from ._frame import Frame
import pygame as pg
import typing as tp


class Label(Frame):
    """
    A thing to display text
    """
    _text_var: Variable = ...
    _text_size: tuple[int, int] = ...

    def __init__(
            self,
            parent: tp.Union["Frame", tp.Any],
            text: str = "Label",
            font_size: int = ...,
            bg: Color = ...,
            fg: Color = ...,
            textvariable: Variable = ...,
            **args
    ) -> None:
        """

        """
        self._text_size = (0, 0)
        self._text_var = arg_or_default(
            textvariable,
            StringVar(value=arg_or_default(text, "Button", ...)),
            ...
        )

        # remove configured arguments
        if "layout" in args:
            args.pop("layout")

        style = Style(
            color=arg_or_default(fg, parent.theme.label.fg),
            backgroundColor=arg_or_default(bg, parent.theme.label.bg),
            fontSize=arg_or_default(font_size, parent.theme.label.font_size)
        )

        # if style option exists, overwrite the default one
        if "style" in args:
            style = style.overwrite(args["style"])

            args.pop("style")

        # initialize parent class
        super().__init__(
            parent=parent,
            layout=Layout.Grid,
            style=style,
            **args
        )

        # initialize font
        # noinspection PyTypeChecker
        self._font = pg.font.SysFont(None, self.style.fontSize)

    @property
    def text_size(self) -> tuple[int, int]:
        return self._text_size

    @property
    def text_variable(self) -> Variable:
        return self._text_var

    def draw(self, surface: pg.Surface) -> None:
        """
        draw the Label
        """
        current_style = self.style

        if self.is_hover:
            current_style = self.style.overwrite(self.hover_style)

        if self.is_active:
            current_style = self.style.overwrite(self.hover_style).overwrite(
                self.active_style
            )

        # get text
        r_text = self._font.render(
            self._text_var.get(),
            True,
            current_style.color.irgba
        )

        width, height = r_text.get_size()
        self._text_size = width, height

        bg_width, bg_height = self.get_size()

        border_radius = max([
            current_style.borderTopLeftRadius,
            current_style.borderTopRightRadius,
            current_style.borderBottomLeftRadius,
            current_style.borderBottomRightRadius
        ])
        frame_size = (
            width + border_radius,
            height + border_radius
        )

        self.configure(min_width=frame_size[0], min_height=frame_size[1])
        self.assigned_width = frame_size[0]
        self.assigned_height = frame_size[1]

        # draw frame
        super().draw(surface)

        # get frame center
        center_x = self._x + bg_width / 2
        center_y = self._y + bg_height / 2

        # center label on frame center
        pos = (
            center_x - width / 2,
            center_y - height / 2
        )

        surface.blit(r_text, pos)

    def configure(
            self,
            text: str = ...,
            textvariable: Variable = ...,
            **kwargs
    ) -> None:
        """
        configure the label properties
        """
        if text is not ...:
            self._text_var.set(text)

        if textvariable is not ...:
            self._text_var = textvariable

    def notify(
            self, event: ThemeManager.NotifyEvent | Style.NotifyEvent,
            info: tp.Any = ...
    ) -> None:
        """
        for notifications from child / parent classes
        """
        match event:
            case GeoNotes.SetHover:
                self.parent.set_hover(True)

            case GeoNotes.SetActive:
                self.parent.set_active(True)
