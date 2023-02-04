"""
_pg_root.py
04. February 2023

the root of the window

Author:
Nilusink
"""
from .theme import ThemeManager
import pygame as pg
import typing as tp

from .types import *


DEFAULT_TITLE: str = "Window"
DEFAULT_ICON: str = "icon.png"


class PgRoot:
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
