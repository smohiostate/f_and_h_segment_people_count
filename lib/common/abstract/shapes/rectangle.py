from common.abstract.shapes import Shape, Drawable

import cv2

class DrawableRectangle(Drawable):

    def cv2_draw(self, cv2_buffer):
        x, y = self.origin.dimensional_components()[:2]

        border_size = 2
        rectangle_width, rectangle_height = self.shape.width - border_size, self.shape.height - border_size

        color_bgr = self.color.bgr_tuple()

        # This is an in-place write, therefore there is no return value.
        cv2.rectangle(cv2_buffer, (int(x), int(y)), (int(x+rectangle_width), int(y+rectangle_height)), color_bgr, border_size)


class Rectangle(Shape):

    __drawable__ = DrawableRectangle

    def __init__(self, width=0.0, height=0.0):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return (self.width * 2) + (self.height * 2)

