from abc import ABCMeta, abstractmethod

class Result(object):

    __metaclass__ = ABCMeta

    def __init__(self, base_result):
        self.base_result = base_result

    @abstractmethod
    def __repr__(self):
        pass

    def get_base_result(self):
        return self.base_result
