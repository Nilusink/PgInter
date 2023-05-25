"""
_image.py
25. May 2023

A widget for displaying images

Author:
Nilusink
"""
from ._frame import Frame
import pygame as pg

# try importing pil. The user shouldn't be forced to install pil, but
# will get an error if they try to use the image widget without having it
# installed
try:
    from PIL import Image
    PIL_EXISTS = True

except ImportError:
    PIL_EXISTS = False


def pi_image_to_surface(pil_image):
    """
    helper function for converting pillow images to pygame images
    """
    return pg.image.fromstring(
        pil_image.tobytes(),
        pil_image.size,
        pil_image.mode
    ).convert()


class ImageFrame(Frame):
    _img: Image.Image

    def __new__(cls, *args, **kwargs):
        if not PIL_EXISTS:
            raise ImportError(
                "PIL needs to be installed to use the Image widget.\n"
                "\tto install PIL, use\n"
                "\t\t\"pip install pillow\""
            )

        return object.__new__(cls)

    def __init__(
            self,
            parent: Frame,
            image: Image,
            *args,
            **kwargs
    ) -> None:
        self._img = image

        super().__init__(parent, *args, **kwargs)

    def draw(self, surface: pg.Surface) -> None:
        """
        insert the image
        """
        width, height = self.get_size()
        image_width, image_height = self._img.size

        # try to reserve aspect angle
        if width <= 0 < height:
            width = int((image_width/image_height) * height)

        if height <= 0 < width:
            height = int((image_height/image_width) * width)

        # if no with or height has yet been set, clone the
        # original image's size
        if width <= 0:
            width = image_width

        if height <= 0:
            height = image_height

        now_image = pi_image_to_surface(self._img.resize((width, height)))
        surface.blit(now_image, (self._x, self._y))

# TODO: more functionality
