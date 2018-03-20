from common.abstract.data import Color

import numpy as np
import scipy.ndimage
import cv2

import math
import base64
import squarify
import cStringIO
from PIL import Image as PILImage
from io import BytesIO

__author__ = 'Baldwin Chang'


class Image(object):

    def __init__(self, np_array_of_colors):
        self._np_array_of_colors = np_array_of_colors
        self._height = len(np_array_of_colors)
        self._width = len(np_array_of_colors[0])

    @classmethod
    def from_list_of_colors(cls, list_of_colors):
        np_array_of_pixels = np.array(list_of_colors)
        return cls(np_array_of_pixels)

    @classmethod
    def from_list_of_pixels(cls, list_of_pixels):
        np_array_of_pixels = np.array([np.array([pixel.to_list() for pixel in row]) for row in list_of_pixels])
        return cls(np_array_of_pixels)

    @classmethod
    def from_base64(cls, base64_source):
        base64_split = base64_source.split(',')
        base64_encoded = base64_split[0] if len(base64_split) == 1 else base64_split[1]
        base64_decoded = base64.b64decode(base64_encoded)
        pil_image = PILImage.open(BytesIO(base64_decoded))
        return cls.from_pil_image(pil_image)

    @classmethod
    def from_file(cls, file_location):
        np_array_of_colors = scipy.ndimage.imread(file_location, mode='RGB')
        return cls(np_array_of_colors)

    @classmethod
    def from_pil_image(cls, pil_image):
        np_array_of_colors = np.array(pil_image.convert('RGB'))
        return cls(np_array_of_colors)

    @classmethod
    def from_cv2_encode(cls, encoded_image):
        np_array_of_colors = cv2.cvtColor(encoded_image, cv2.COLOR_BGR2RGB)
        return cls(np_array_of_colors)

    def get_np_array(self):
        return self._np_array_of_colors

    def get_sub_image(self, start_x, start_y, width, height):
        left_boundary = min(max(0, start_x), self.width())
        right_boundary = min(left_boundary + width, self.width())
        top_boundary = min(max(0, start_y), self.height())
        bottom_boundary = min(top_boundary + height, self.height())

        sub_image_np_array_of_colors = self._np_array_of_colors[top_boundary:bottom_boundary, left_boundary:right_boundary]
        return Image(sub_image_np_array_of_colors)

    def _get_normalized_sub_image_areas(self, area_of_sub_images):
        minimum_number_of_sub_images = int(math.floor(self.area() / area_of_sub_images))
        naive_area_sizes = [area_of_sub_images] * minimum_number_of_sub_images
        normalized_area_sizes = squarify.normalize_sizes(naive_area_sizes, self.width(), self.height())
        calculated_rectangles = squarify.squarify(normalized_area_sizes, 0, 0, self.width(), self.height())

        return calculated_rectangles

    def divide_by_area(self, area_of_sub_images):
        sub_images = list()

        if area_of_sub_images >= self.area():
            sub_images.append(self)
        else:

            calculated_rectangles = self._get_normalized_sub_image_areas(area_of_sub_images)

            for rectangle in calculated_rectangles:
                start_x = int(math.floor(rectangle['x']))
                start_y = int(math.floor(rectangle['y']))
                width = int(math.floor(rectangle['dy']))
                height = int(math.floor(rectangle['dx']))

                sub_images.append(self.get_sub_image(start_x, start_y, width, height))

        return sub_images

    def crop(self, x_top, y_top, x_bottom, y_bottom):
        pil_image = self.to_pil_image()
        pil_image = pil_image.crop((x_top, y_top, x_bottom, y_bottom))
        return Image.from_pil_image(pil_image)

    def resize(self, width, height, method=PILImage.ANTIALIAS):
        pil_image = self.to_pil_image()
        pil_image = pil_image.resize((width, height), method)
        return Image.from_pil_image(pil_image)

    def cv2_encode(self):
        return cv2.cvtColor(self.get_np_array(), cv2.COLOR_RGB2BGR)

    def to_binary(self, encoder_ext='.jpg'):
        return cv2.imencode(encoder_ext, self.cv2_encode())[1].tostring()

    def to_pil_image(self):
        return PILImage.fromarray(self.get_np_array(), 'RGB')

    def to_colors(self):
        return np.array([np.array([Color(*column) for column in row]) for row in self.get_np_array()])

    def to_base64(self, image_format="GIF"):
        pil_image = self.to_pil_image()
        buffer_io = cStringIO.StringIO()
        pil_image.save(buffer_io, image_format)
        return base64.b64encode(buffer_io.getvalue())

    def height(self):
        return self._height

    def width(self):
        return self._width

    def area(self):
        return self._width * self._height
