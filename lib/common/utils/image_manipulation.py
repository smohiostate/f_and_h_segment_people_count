from common.abstract.shapes.rectangle import Rectangle
from common.abstract.cartesian import Coordinate

from common.constants import DEFAULT_BOUNDING_BOX_COLOR, DEFAULT_CLASSIFICATION_COLOR

def draw_bounding_box_on_image(image, bounding_box=None, color=DEFAULT_BOUNDING_BOX_COLOR):
    if bounding_box is None:
        start_x, start_y, width, height = 0, 0, image.width(), image.height()
    else:
        start_x, start_y, width, height = bounding_box

    origin = Coordinate(start_x, start_y)
    rectangle = Rectangle(width=width, height=height)
    drawer = rectangle.get_drawable(origin=origin, color=color)

    return drawer.draw(image)


def draw_spatial_results_on_image(image, spatial_results, color=DEFAULT_CLASSIFICATION_COLOR):
    annotated_image = image

    for result in spatial_results:
        drawer = result.get_drawable(color=color)
        annotated_image = drawer.draw(annotated_image)

    return annotated_image
