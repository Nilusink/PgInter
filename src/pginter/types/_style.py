"""
_style.py
11. May 2023

The style of one element

Author:
Nilusink
"""
from ._geo_types import Layout
from ._color import Color
import typing as tp


class Style:
    """
    What would a UI be without styles? Correct, a terminal!
    """
    width: int = ...
    height: int = ...
    minWidth: int = ...
    minHeight: int = ...

    color: Color = ...
    backgroundColor: Color = ...

    layout: Layout = ...
    margin: int = ...
    padding: int = ...

    borderRadius: int = ...
    borderBottom_radius: int = ...
    borderTopRadius: int = ...
    borderBottomLeftRadius: int = ...
    borderBottomRightRadius: int = ...
    borderTopLeftRadius: int = ...
    borderTopRightRadius: int = ...
    borderWidth: int = ...
    borderColor: Color = ...

    fontSize: int = ...

    def __init__(
            self,
            width: int = ...,
            height: int = ...,
            minWidth: int = ...,
            minHeight: int = ...,
            color: Color = ...,
            backgroundColor: Color = ...,
            layout: Layout = ...,
            margin: int = ...,
            padding: int = ...,
            borderRadius: int = ...,
            borderBottom_radius: int = ...,
            borderTopRadius: int = ...,
            borderBottomLeftRadius: int = ...,
            borderBottomRightRadius: int = ...,
            borderTopLeftRadius: int = ...,
            borderTopRightRadius: int = ...,
            borderWidth: int = ...,
            borderColor: Color = ...,
            fontSize: int = ...,
    ) -> None:
        """
        create a style element
        """
        self.width = width
        self.height = height
        self.minWidth = minWidth
        self.minHeight = minHeight
        self.color = color
        self.backgroundColor = backgroundColor
        self.layout = layout
        self.margin = margin
        self.padding = padding
        self.borderRadius = borderRadius
        self.borderBottom_radius = borderBottom_radius
        self.borderTopRadius = borderTopRadius
        self.borderBottomLeftRadius = borderBottomLeftRadius
        self.borderBottomRightRadius = borderBottomRightRadius
        self.borderTopLeftRadius = borderTopLeftRadius
        self.borderTopRightRadius = borderTopRightRadius
        self.borderWidth = borderWidth
        self.borderColor = borderColor
        self.fontSize = fontSize

    @classmethod
    def from_dict(cls, ignore_invalid: bool = False, **properties) -> tp.Self:
        """
        Create a style element from a dict.
        """
        new_instance = cls()

        for prop, value in properties.items():
            try:
                new_instance[prop] = value

            except KeyError:
                if ignore_invalid:
                    continue

                raise

        return new_instance

    @property
    def properties(self) -> list[str]:
        """
        all available style properties
        """
        out = []
        for prop in self.__dict__:
            if prop.startswith("__") or prop.endswith("__"):
                continue

            if hasattr(self, prop):
                out.append(prop)

        return out

    def overwrite(self, other: tp.Self) -> tp.Self:
        """
        "merge" two styles, choosing the "other" styles values
        for doubles
        """
        new_instance = self.__class__()
        for prop in self.properties:
            # if available, use "other" style
            if other[prop] is not ...:
                new_instance[prop] = other[prop]

            # if "other" isn't available, try own style
            elif self[prop] is not ...:
                new_instance[prop] = self[prop]

        return new_instance

    # accessibility
    def __getitem__(self, item: str) -> tp.Any:
        if item in self.properties:
            return self.__dict__[item]

        raise KeyError(f"Can't find item \"{item}\" in Style.")

    def __setitem__(self, key: str, value: tp.Any) -> None:
        if key in self.properties:
            self.__dict__[key] = value

        raise KeyError(f"Can't find item \"{key}\" in Style.")
