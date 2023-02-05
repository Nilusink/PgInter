"""
_pg_root.py
04. February 2023

the root of the window

Author:
Nilusink
"""
import os.path

from .widgets import GeometryManager
from .theme import ThemeManager
import pygame as pg
import typing as tp

from .types import *


DEFAULT_TITLE: str = "Window"
DEFAULT_ICON: str = os.path.dirname(__file__) + "/icon.png"


class PgRoot(GeometryManager):
    _running: bool = True
    _theme: ThemeManager = ...
    __background: pg.Surface = ...

    def __init__(
            self,
            title: str = ...,
            icon_path: str = ...,
            size: tuple[int, int] = ...,
            bg_color: Color = ...,
    ):
        super().__init__()
        self._theme = ThemeManager()

        # args
        self._bg = self._theme.root.bg.hex if bg_color is ... else bg_color

        # pg init
        pg.init()
        pg.font.init()

        self.__background = pg.display.set_mode()

        # set icon and caption
        pg.display.set_caption(DEFAULT_TITLE if title is ... else title)
        img = pg.image.load(DEFAULT_ICON if icon_path is ... else icon_path, "icon")
        pg.display.set_icon(img)

    # config
    @property
    def title(self) -> str:
        return pg.display.get_caption()[0]

    @title.setter
    def title(self, value: str) -> None:
        pg.display.set_caption(value)

    @property
    def theme(self) -> ThemeManager:
        return self._theme

    # pygame stuff
    def _event_handler(self) -> None:
        """
        handle the events raised by pygame
        """
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self._running = False

    def update_screen(self) -> None:
        """
        update the screen
        """
        self.__background.fill(self._bg)

        self.calculate_geometry()
        for child, params in self._child_params:
            child.draw(self.__background)

        pg.display.flip()

    def update(self) -> None:
        """
        update events
        """
        self._event_handler()

    def mainloop(self):
        """
        run the windows main loop
        """
        while self._running:
            self.update()
            self.update_screen()

    def calculate_geometry(self):
        """
        calculate how each individual child should be placed
        """
        match self._layout:
            case 0:  # Absolute
                # since the positioning is absolute, the children should not influence the parents size
                for child, params in self._child_params:
                    child.set_position(params.x, params.y)

                return

            case 1:
                ...

            case 2:
                ...

            case _:
                raise ValueError(f"Invalid geometry type: {self._layout.__class__.__name__}")

    def calculate_size(self) -> tuple[int, int]:
        """
        calculate how big the container should be
        """
        # make sure the geometry is up-to-date
        self.calculate_geometry()

        return pg.display.get_window_size()
