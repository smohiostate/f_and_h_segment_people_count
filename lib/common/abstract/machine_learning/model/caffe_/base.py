from abc import ABCMeta

from common.abstract.machine_learning.model import Model
from common.abstract.machine_learning.device import CPUDevice, GPUDevice

import caffe

class CaffeModel(Model):

    __metaclass__ = ABCMeta

    def __init__(self, device):
        super(CaffeModel, self).__init__()

        if type(device) is GPUDevice:
            caffe.set_device(device.get_id())
            caffe.set_mode_gpu()
        else:
            caffe.set_mode_cpu()



