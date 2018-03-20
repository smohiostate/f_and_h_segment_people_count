from common.abstract.machine_learning.result import Result

from common.abstract.shapes import Label, Composable


class SpatialResult(Result):

    def __init__(self, label, score, shape, origin):
        super(SpatialResult, self).__init__(base_result=(label, score, shape, origin))
        self.label = str(label)
        self.score = str(score)
        self.shape = shape
        self.origin = origin

    def __repr__(self):
        return 'SpatialResult(label={}, score={}, shape={}, origin={})'.format(self.label, self.score, self.shape, self.origin)

    def get_label(self):
        return self.label

    def get_score(self):
        return self.score

    def get_shape(self):
        return self.shape

    def get_origin(self):
        return self.origin

    def get_drawable(self, color):
        label_shape = Label('{} - {}'.format(self.label, self.score))
        return Composable(*[shape.get_drawable(origin=self.origin, color=color) for shape in (self.shape, label_shape)])
