from abc import ABCMeta, abstractmethod

from common.abstract.data import Image

import copy

class Shape(object):

    __metaclass__ = ABCMeta
    __drawable__ = None

    def get_drawable(self, origin, color):
        return self.__drawable__(shape=self, origin=origin, color=color)


class Drawable(object):
    """
        Provides a simple interface for shapes to
        create a drawable object.
    """

    def __init__(self, shape, origin, color):
        self.shape = shape
        self.origin = origin
        self.color = color

    def draw(self, image):
        cv2_buffer = copy.deepcopy(image.cv2_encode())
        self.cv2_draw(cv2_buffer)
        return Image.from_cv2_encode(cv2_buffer)

    @abstractmethod
    def cv2_draw(self, cv2_buffer):
        pass


class Composable(object):

    def __init__(self, *drawables):
        self.drawables = drawables

    def draw(self, image):
        intermediate_image = image

        for drawer in self.drawables:
            intermediate_image = drawer.draw(intermediate_image)

        return intermediate_image
