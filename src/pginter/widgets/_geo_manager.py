"""
_geo_manager.py
04. February 2023

How children are placed

Author:
Nilusink
"""
from _supports_children import SupportsChildren
from ..types import Absolute, Pack, Grid
import typing as tp


class GeometryManager(SupportsChildren):
    """
    Manages how children are placed inside a parent container
    """
    _layout: int = Absolute
    _child_params: list[tuple[tp.Any, dict]]

    def __init__(self, layout: int = ...):
        super().__init__()

        self._layout = Absolute if layout is ... else layout

    def add_child(self, child: tp.Any, **params) -> None:
        """
        add a child to the collection
        """
        if child not in self._children:
            super().add_child(child)
            self._child_params.append((child, params))

    def calculate_geometry(self) -> tuple[float, float]:
        """
        calculate how each individual child should be placed
        """
        match self._layout:
            case 0:  # Absolute
                # since the positioning is absolute, the children should not influence the parents size
                return

            case 1:
                ...

            case 2:
                ...

            case _:
                raise ValueError(f"Invalid geometry type: {self._layout.__class__.__name__}")
