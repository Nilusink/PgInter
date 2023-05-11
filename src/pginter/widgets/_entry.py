"""
_entry.py
22. February 2023

<description>

Author:
Nilusink
"""
from ..types import Color, Layout
from ._label import Label
from ._frame import Frame
import typing as tp


class Entry(Frame):
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
            min_width=100,
            min_height=10,
            **kwargs
        )
        self.set_layout(Layout.Grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._label = Label(
            parent=self,
            text="Entry",
        )
        self._label.grid(row=0, column=0)
