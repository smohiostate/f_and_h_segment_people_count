from common.abstract.machine_learning.result import Result
from common.abstract.machine_learning.result.objects import SpatialResult
from tffrcnn.fast_rcnn.nms_wrapper import nms

from common.utils.data_manipulation import parse_bounding_box
from common.abstract.cartesian import Coordinate
from common.abstract.shapes import Rectangle

from common.constants import NUMBER_OF_BOX_POINTS, DEFAULT_CONFIDENCE_THRESHOLD, \
    DEFAULT_OVERLAP_THRESHOLD

import numpy as np

class ObjectsIntermediateResult(Result):

    scores = np.array([ [] ])
    boxes = np.array([ [] ])

    def __init__(self, scores=None, boxes=None):
        super(ObjectsIntermediateResult, self).__init__((scores, boxes))
        self.scores = scores
        self.boxes = boxes

    # TODO: write an informative string representation to help debugging
    def __repr__(self):
        return 'ObjectsIntermediateResult(|Scores|={}, |Boxes|={})'.format(self.scores.shape, self.boxes.shape)

    def get_scores(self):
        return self.scores

    def get_boxes(self):
        return self.boxes

    def get_scores_for_class_index(self, class_index):
        """
        get_scores_for_class_index() returns the
        appropriate classification score for the given class_index
        """
        class_scores = self.scores[:, class_index]
        return class_scores

    def get_boxes_for_class_index(self, class_index):
        """
        get_boxes_for_class_index() returns the
        appropriate bounding box points for the given class_index
        """
        adjusted_class_box_index = lambda index: NUMBER_OF_BOX_POINTS * index
        class_boxes = self.boxes[:, adjusted_class_box_index(class_index):adjusted_class_box_index(class_index + 1)]
        return class_boxes

    def process_singular_class_index(self, class_index, label=None, overlap_threshold=DEFAULT_OVERLAP_THRESHOLD, confidence_threshold=DEFAULT_CONFIDENCE_THRESHOLD):
        result_label = label if label is not None else class_index
        scores = self.get_scores_for_class_index(class_index)
        boxes = self.get_boxes_for_class_index(class_index)

        nms_vector = non_maximal_suppression(scores, boxes, overlap_threshold)
        classification_vector = filter_non_maximum_suppression_result(nms_vector, confidence_threshold)

        results = list()

        for classification in classification_vector:
            x_top, y_top, x_bottom, y_bottom = classification[:4]
            score = classification[-1]

            x_top, y_top, width, height = parse_bounding_box(x_top, y_top, x_bottom, y_bottom)
            shape = Rectangle(width=width, height=height)
            origin = Coordinate(x_top, y_top)

            spatial_result = SpatialResult(label=result_label, score=score, shape=shape, origin=origin)

            results.append(spatial_result)

        return results


def non_maximal_suppression(scores_vector, boxes_vector, overlap_threshold):
    """
    non_maximal_suppression() will take your score and box vectors, flatten them,
    and return a vector that meets the specified threshold
    """
    flattened_vector = np.hstack((boxes_vector, scores_vector[:, np.newaxis])).astype(np.float32)
    non_suppressed_objects_indices = nms(flattened_vector, overlap_threshold)
    non_suppressed_objects_vector = flattened_vector[non_suppressed_objects_indices, :]
    return non_suppressed_objects_vector


def filter_non_maximum_suppression_result(nms_vector, confidence_threshold):
    indices = np.where(nms_vector[:, -1] >= confidence_threshold)[0]
    return nms_vector[indices]

