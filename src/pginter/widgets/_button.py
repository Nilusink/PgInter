"""
_button.py
08. March 2023

Something you can click

Author:
Nilusink
"""
from ..types import Color, Layout, Style, GeoNotes, Variable
from ..utils import arg_or_default
from ..theme import ThemeManager
from ._label import Label
from ._frame import Frame
import typing as tp


class Button(Frame):
    _label: Label = ...
    _command: tp.Callable[[], None] = ...
    _text_var: Variable = ...

    def __init__(
            self,
            parent: tp.Union["Frame", tp.Any],
            *,
            bg: Color = ...,
            fg: Color = ...,
            text: str = "Button",
            width: int = ...,
            height: int = ...,
            command: tp.Callable[[], None] = ...,
            textvariable: Variable = ...,
            **kwargs
    ) -> None:
        """

        """
        self._command = command
        self._text_var = textvariable

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

        self.style.color = arg_or_default(fg, Color.white(), ...)
        self.hover_style.backgroundColor = Color.from_hex("#888")
        self.active_style.backgroundColor = Color.from_hex("#bbb")

        self._label = Label(
            parent=self,
            text=text,
            textvariable=textvariable,
            fg=fg,
            style=Style(backgroundColor=Color.transparent())
        )
        self._label.grid(row=0, column=0, sticky="nsew")

        self.style.notify_on(
            "color",
            lambda _, key: self._sync_label_style(key, "normal")
        )

        self.hover_style.notify_on(
            "color",
            lambda _, key: self._sync_label_style(key, "hover")
        )

        self.active_style.notify_on(
            "color",
            lambda _, key: self._sync_label_style(key, "active")
        )

        # first time style sync
        self._sync_label_style("color", "normal")
        self._sync_label_style("color", "hover")
        self._sync_label_style("color", "active")

    def draw(self, surface) -> None:
        super().draw(surface)

    def _sync_label_style(
            self,
            key: str,
            style_type: tp.Literal["normal", "hover", "active"] = "normal"
    ) -> None:
        """
        sync a label style with the button style
        """
        if style_type == "normal":
            self._label.style[key] = self.style[key]

        elif style_type == "hover":
            self._label.hover_style[key] = self.hover_style[key]

        elif style_type == "active":
            self._label.active_style[key] = self.active_style[key]

        else:
            raise ValueError("Invalid label sync type: ", style_type)

    def notify(
            self,
            event: ThemeManager.NotifyEvent | Style.NotifyEvent,
            info: tp.Any = ...
    ) -> None:
        match event:
            case GeoNotes.SetActive:
                # catch setActive event for handling the command
                if not self.is_active and self._command is not ...:
                    self._command()

                super().notify(event, info)

            case _:
                super().notify(event, info)

