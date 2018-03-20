__author__ = 'Baldwin Chang'


class Color(object):

    def __init__(self, red=0, green=0, blue=0, alpha=0):
        self._red = red
        self._green = green
        self._blue = blue
        self._alpha = alpha

    @classmethod
    def from_rgb(cls, red=0, green=0, blue=0):
        return cls(red, green, blue)

    @classmethod
    def from_bgr(cls, blue=0, green=0, red=0):
        return cls(red, green, blue)

    def __repr__(self):
        return 'Pixel(R={}, G={}, B={}, alpha={})'.format(self._red, self._green, self._blue, self._alpha)

    def to_list(self):
        return [self._red, self._green, self.blue, self._alpha]

    def red(self):
        return self._red

    def green(self):
        return self._green

    def blue(self):
        return self._blue

    def alpha(self):
        return self._alpha

    def rgb_tuple(self):
        return self.red(), self.green(), self.blue()

    def bgr_tuple(self):
        return self.blue(), self.green(), self.red()
