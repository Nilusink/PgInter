"""
_geo_manager.py
04. February 2023

How children are placed

Author:
Nilusink
"""
from ..types import Absolute, Pack, Grid, BetterDict
from ._supports_children import SupportsChildren
import typing as tp


class GeometryManager(SupportsChildren):
    """
    Manages how children are placed inside a parent container
    """
    _layout: int = Absolute
    _width: float = -1   # -1 means not configured -> takes minimum size required by its children
    _height: float = -1  # or the size it gets by the parents geometry manager
    _child_params: list[tuple[tp.Any, BetterDict]] = ...

    def __init__(self, layout: int = ...):
        super().__init__()

        self._layout = Absolute if layout is ... else layout
        self._child_params = []

    def set_layout(self, layout: int) -> None:
        """
        set the container's layout type
        """
        if layout not in (Absolute, Pack, Grid):
            raise ValueError("Invalid container layout: ", layout)

        self._layout = layout

    def add_child(self, child: tp.Any, **params) -> None:
        """
        add a child to the collection
        """
        if child not in self._children:
            super().add_child(child)
            self._child_params.append((child, BetterDict(params)))

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

        match self._layout:
            case 0:  # Absolute
                # since the positioning is absolute, the children should not influence the parents size
                return self._width.__floor__(), self._height.__floor__()

            case 1:
                ...

            case 2:
                ...

            case _:
                raise ValueError(f"Invalid geometry type: {self._layout.__class__.__name__}")
