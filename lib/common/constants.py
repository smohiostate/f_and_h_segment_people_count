from common.abstract.data import Color
from common.abstract.cartesian import Coordinate

DEFAULT_COLOR = Color(red=0, green=0, blue=0)
DEFAULT_BOUNDING_BOX_COLOR = Color(green=255)
DEFAULT_CLASSIFICATION_COLOR = Color(blue=255)

DEFAULT_ORIGIN = Coordinate(0, 0)

NUMBER_OF_BOX_POINTS = 4
DEFAULT_CONFIDENCE_THRESHOLD = 0.8
DEFAULT_OVERLAP_THRESHOLD = 0.3
