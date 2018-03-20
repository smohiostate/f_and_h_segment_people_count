from common.abstract.machine_learning.result import Result

class ClassificationResult(Result):

    predicted_label = None
    probability = 0.0

    def __init__(self, label=None, score=0.0):
        self.label = label
        self.score = score
        super(ClassificationResult, self).__init__((label, score))

    def __repr__(self):
        return 'ClassificationResult(label={}, score={})'.format(self.label, self.score)

    def get_label(self):
        return self.label

    def get_score(self):
        return self.score
