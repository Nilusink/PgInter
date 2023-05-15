"""
_button.py
08. March 2023

Something you can click

Author:
Nilusink
"""


from ..types import Color, Layout, Style, GeoNotes
from ..theme import ThemeManager
from ._label import Label
from ._frame import Frame
import typing as tp


class Button(Frame):
    _label: Label = ...

    def __init__(
            self,
            parent: tp.Union["Frame", tp.Any],
            width: int = ...,
            height: int = ...,
            bg: Color = ...,
            fg: Color = ...,
            **kwargs
    ) -> None:
        """

        """
        super().__init__(
            parent=parent,
            width=width,
            height=height,
            bg=bg,
            min_width=20,
            min_height=20,
            **kwargs
        )
        self.set_layout(Layout.Grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.hover_style.backgroundColor = Color.from_hex("#aaa")
        self.active_style.backgroundColor = Color.from_hex("#fff")

        self._label = Label(
            parent=self,
            text="Button",
            fg=fg,
            bg=Color.transparent()
        )
        self._label.grid(row=0, column=0, sticky="nsew")

    def notify(
            self,
            event: ThemeManager.NotifyEvent | Style.NotifyEvent,
            info: tp.Any = ...
    ) -> None:
        match event:
            case GeoNotes.SetHover:
                self._is_hover = True
                self._is_active = False

            case GeoNotes.SetActive:
                self._is_hover = False
                self._is_active = True

            case GeoNotes.SetNormal:
                self._is_hover = False
                self._is_active = False

            case _:
                super().notify(event, info)

