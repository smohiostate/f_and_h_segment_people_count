from abc import ABCMeta, abstractmethod
from common.abstract.machine_learning.device import Device


class CPUDevice(Device):

    __metaclass__ = ABCMeta

    def __init__(self):
        super(CPUDevice, self).__init__()


