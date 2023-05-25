"""
_surface_frame.py
24. May 2023

A pygame surface to draw on

Author:
Nilusink
"""
from ._frame import Frame
import typing as tp
import pygame as pg


class SurfaceFrame(Frame):
    """
    A pygame surface to draw on
    """
    _surface: pg.Surface

    def __init__(
            self,
            parent: tp.Union["Frame", tp.Any],
            width: int = ...,
            height: int = ...,
            margin: int = ...,
            min_width: int = ...,
            min_height: int = ...,
    ) -> None:

        # limit the arguments that get passed to the parent
        super().__init__(
            parent=parent,
            width=width,
            height=height,
            margin=margin,
            min_width=min_width,
            min_height=min_height
        )

    @property
    def surface(self) -> pg.Surface:
        return self._surface

    def draw(self, surface: pg.Surface) -> None:
        """
        insert the surface
        """
        surface.blit(self._surface, (self._x, self._y))
