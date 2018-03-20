from common.abstract.data.pixel import Color
from common.abstract.data.image import Image

# Pixel

def test_pixel_components():
    pixel = Color(red=200, green=100, blue=200)
    assert pixel.red() == 200
    assert pixel.green() == 100
    assert pixel.blue() == 200


# Image

def test_image_width():
    black_pixel = Color(red=0, green=0, blue=0)
    image = Image.from_list_of_pixels([[black_pixel], [black_pixel]])
    assert image.width() == 1


def test_image_height():
    black_pixel = Color(red=0, green=0, blue=0)
    image = Image.from_list_of_pixels([[black_pixel], [black_pixel]])
    assert image.height() == 2

def test_image_resize():
    black_pixel = Color(red=0, green=0, blue=0)
    image = Image.from_list_of_pixels([[black_pixel], [black_pixel]])
    image_resize = image.resize(200, 200)
    assert image_resize.height() == 200
    assert image_resize.width() == 200

