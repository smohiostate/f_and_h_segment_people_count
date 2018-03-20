from abc import ABCMeta, abstractmethod

from common.abstract.machine_learning.device import CPUDevice, GPUDevice

from common.abstract.machine_learning.model.tensorflow_ import TensorFlowModel

from common.abstract.machine_learning.result.objects import ObjectsIntermediateResult

from tffrcnn.fast_rcnn.test import im_detect

from tffrcnn.fast_rcnn.config import cfg

class TensorFlowFastRCNNModel(TensorFlowModel):

    __metaclass__ = ABCMeta

    # Define a Fast-RCNN Network
    network = None

    use_gpu = False

    def __init__(self, device=None):
        super(TensorFlowFastRCNNModel, self).__init__(device=device)

        if type(device) is GPUDevice:
            cfg.USE_GPU_NMS = self.use_gpu = True
        else:
            cfg.USE_GPU_NMS = self.use_gpu = False

    def detect_object_proposals(self, x_cv2_image):
        scores, boxes = im_detect(self.session, self.network, x_cv2_image)
        intermediate_result = ObjectsIntermediateResult(scores=scores, boxes=boxes)

        return intermediate_result
