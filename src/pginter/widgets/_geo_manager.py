"""
_geo_manager.py
04. February 2023

How children are placed

Author:
Nilusink
"""
from ..types import Absolute, Pack, Grid, BetterDict, TOP, BOTTOM, LEFT, RIGHT
from ._supports_children import SupportsChildren
from copy import deepcopy
import typing as tp


class GeometryManager(SupportsChildren):
    """
    Manages how children are placed inside a parent container
    """
    _layout: int = Absolute
    _width: float = -1   # -1 means not configured -> takes minimum size required by its children
    _height: float = -1  # or the size it gets by the parents geometry manager
    _width_configured: bool = False
    _height_configured: bool = False
    _child_params: list[tuple[tp.Any, BetterDict]] = ...
    _layout_params: BetterDict = ...

    def __init__(
            self,
            layout: int = ...,
            margin: int = 0,
            padding: int = 0
    ):
        super().__init__()

        self._layout = Absolute if layout is ... else layout
        self._layout_params = BetterDict({
            "margin": margin,
            "padding": padding
        })
        self._child_params = []

    @property
    def layout(self) -> int:
        """
        the containers layout type
        """
        return self._layout

    @property
    def width(self) -> float:
        return self._width
    
    @width.setter
    def width(self, value: float) -> None:
        self._width = value
        self._width_configured = True

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value
        self._height_configured = True

    def set_layout(self, layout: int) -> None:
        """
        set the container's layout type
        """
        if layout not in (Absolute, Pack, Grid):
            raise ValueError("Invalid container layout: ", layout)

        if len(self._child_params) > 0:
            # if children are already present, delete them
            for child, _param in self._child_params:
                child.delete()

            self._child_params.clear()

            raise RuntimeWarning("changing layout with children already present!")

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

            case 1:  # pack
                directional_dict: dict[str, int | list] = {"total_x": 0, "total_y": 0, "children": [], "sizes": []}
                top = deepcopy(directional_dict)
                bottom = deepcopy(directional_dict)
                left = deepcopy(directional_dict)
                right = deepcopy(directional_dict)

                # get all sizes and group by anchor
                for child, param in self._child_params:
                    child_size = child.calculate_size()

                    if param.anchor == TOP:
                        top["children"].append(child)
                        top["sizes"].append(child_size)
                        top["total_x"] += child_size[0]
                        top["total_y"] += child_size[1]

                    elif param.anchor == BOTTOM:
                        bottom["children"].append(child)
                        bottom["sizes"].append(child_size)
                        bottom["total_x"] += child_size[0]
                        bottom["total_y"] += child_size[1]

                    elif param.anchor == LEFT:
                        left["children"].append(child)
                        left["sizes"].append(child_size)
                        left["total_x"] += child_size[0]
                        left["total_y"] += child_size[1]

                    elif param.anchor == RIGHT:
                        right["children"].append(child)
                        right["sizes"].append(child_size)
                        right["total_x"] += child_size[0]
                        right["total_y"] += child_size[1]

                top["total_y"] += self._layout_params.padding * len(top["children"]) - 1
                bottom["total_y"] += self._layout_params.padding * len(bottom["children"]) - 1

                left["total_x"] += self._layout_params.padding * len(left["children"]) - 1
                right["total_x"] += self._layout_params.padding * len(right["children"]) - 1

                # if not configured, set own size
                total_x = max([top["total_x"], bottom["total_x"], left["total_x"] + right["total_x"]])
                total_y = max([left["total_y"], right["total_y"], top["total_y"] + bottom["total_y"]])

                # add margin
                total_x += self._layout_params.margin * 2
                total_y += self._layout_params.margin * 2

                if not self._width_configured:
                    self._width = total_x

                else:
                    total_x = self._width
    
                if not self._height_configured:
                    self._height = total_y

                else:
                    total_y = self.height

                # tell the children where they should be
                y_cen = total_y / 2
                x_cen = total_x / 2

                # left
                x_now = self._layout_params.margin
                for child, size in zip(left["children"], left["sizes"]):
                    child.set_position(x_now, y_cen - size[1] / 2)
                    x_now += size[0] + self._layout_params.padding

                # right
                x_now = total_x - self._layout_params.margin
                for child, size in zip(right["children"], right["sizes"]):
                    child.set_position(x_now - size[0], y_cen - size[1] / 2)
                    x_now -= size[0] + self._layout_params.padding

                # top
                y_now = self._layout_params.margin
                for child, size in zip(top["children"], top["sizes"]):
                    child.set_position(x_cen - size[0] / 2, y_now)
                    y_now += size[1] + self._layout_params.padding

                # bottom
                y_now = total_y - self._layout_params.margin
                for child, size in zip(bottom["children"], bottom["sizes"]):
                    child.set_position(x_cen - size[0] / 2, y_now - size[1])
                    y_now -= size[1] + self._layout_params.padding

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

        return self._width.__floor__(), self._height.__floor__()
