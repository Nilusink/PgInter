"""
_label.py
10. February 2023

A thing to display text

Author:
Nilusink
"""
from ..types import Color, BetterDict, Layout
from ..utils import arg_or_default
from ._frame import Frame
import pygame as pg
import typing as tp


class LabelConfig(tp.TypedDict):
    font_size: int
    text: str
    fg: str


class Label(Frame):
    """
    A thing to display text
    """
    _config: BetterDict = ...

    def __init__(
            self,
            parent: tp.Union["Frame", tp.Any],
            text: str = "Label",
            font_size: int = ...,
            bg: Color = ...,
            fg: Color = ...,
            **args
    ) -> None:
        """

        """
        # remove configured arguments
        if "layout" in args:
            args.pop("layout")

        # initialize parent class
        super().__init__(
            parent=parent,
            bg=arg_or_default(bg, parent.theme.label.bg),
            layout=Layout.Grid,
            **args
        )

        # arguments
        config: LabelConfig = {
            "font_size": arg_or_default(font_size, self.theme.label.font_size),
            "text": text,
            "fg": arg_or_default(fg, self.theme.label.fg)
        }

        self._config = BetterDict(config)

        self._font = pg.font.SysFont(None, self._config.font_size)

    def draw(self, surface: pg.Surface) -> None:
        """
        draw the Label
        """
        # get text
        r_text = self._font.render(
            self._config.text,
            True,
            self._config.fg.rgba
        )

        width, height = r_text.get_size()
        bg_width, bg_height = self.get_size()

        border_radius = max([
            self.style.borderTopLeftRadius,
            self.style.borderTopRightRadius,
            self.style.borderBottomLeftRadius,
            self.style.borderBottomRightRadius
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
