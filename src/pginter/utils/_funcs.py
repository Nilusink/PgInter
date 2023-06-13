"""
_funcs.py
05. February 2023

a few generic useful functions

Author:
Nilusink
"""
from PIL import Image
from PIL.Image import getmodebase, new, isImageType
import typing as tp


def arg_or_default(
        value: tp.Any,
        default_value: tp.Any,
        check_if: tp.Any = ...
) -> tp.Any:
    """
    :param value: the value to check
    :param default_value: what the value should be if it equals `check_if`
    :param check_if: what to check for
    """
    return default_value if value is check_if else value


def point_in_box(
        point: tuple[int, int],
        box: tuple[int, int, int, int]
) -> bool:
    """
    check if a point is inside a box

    :param point: point to check
    :param box: x, y width, height
    """
    return all([
        # x collision
        box[0] <= point[0],
        point[0] <= box[0] + box[2],

        # y collision
        box[1] <= point[1],
        point[1] <= box[1] + box[3]
    ])


def merge_alphas(
        a: Image,
        b: Image,
        opr: tp.Callable[[float, float], float]
) -> Image:
    """
    merge the alpha channels of two images

    :param a: first alpha
    :param b: second alpha
    :param opr: operation to merge the channels
    """
    im_a = a.load()
    im_b = b.load()
    width, height = a.size

    alpha = Image.new('L', (width, height))
    im = alpha.load()
    for x in range(width):
        for y in range(height):
            im[x, y] = opr(im_a[x, y], im_b[x, y])

    return alpha

