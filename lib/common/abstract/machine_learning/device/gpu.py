from abc import ABCMeta
from common.abstract.machine_learning.device import Device


class GPUDevice(Device):

    __metaclass__ = ABCMeta

    def __init__(self, device_path=None):
        self._device_path = device_path
        super(GPUDevice, self).__init__()

    def get_device_path(self):
        return self._device_path


