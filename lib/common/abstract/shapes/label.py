from common.abstract.shapes import Shape, Drawable

from common.abstract.data import Color

import cv2


class DrawableLabel(Drawable):

    def cv2_draw(self, cv2_buffer):
        x, y = self.origin.dimensional_components()[:2]

        thickness = 1
        padding = 2
        text_color = Color(red=255, green=255, blue=255)
        text_color_bgr = text_color.bgr_tuple()
        background_color_bgr = self.color.bgr_tuple()

        text_width, text_height = cv2.getTextSize(self.shape.text, self.shape.font, self.shape.size, thickness)[0]

        # This is an in-place write, therefore there is no return value.
        cv2.rectangle(cv2_buffer, (int(x), int(y)), (int(x + text_width + (padding * 2)), int(y + text_height + (padding * 2))), background_color_bgr, cv2.FILLED)
        cv2.putText(cv2_buffer, self.shape.text, (int(x + padding), int(y + text_height)), self.shape.font, self.shape.size, text_color_bgr, thickness,
                    cv2.LINE_AA)


class Label(Shape):

    __drawable__ = DrawableLabel

    def __init__(self, text, size=0.5, font=cv2.FONT_HERSHEY_DUPLEX):
        self.text = text
        self.size = size
        self.font = font
