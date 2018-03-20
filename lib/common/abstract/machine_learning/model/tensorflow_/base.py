from abc import ABCMeta

from common.abstract.machine_learning.model import Model
from common.abstract.machine_learning.device import CPUDevice, GPUDevice

import tensorflow as tf


class TensorFlowModel(Model):

    __metaclass__ = ABCMeta

    session = None

    # Trained TensorFlow Parameters
    saver_state_file = None

    # TODO: allow the parameterization of device to be utilized
    def __init__(self, device):
        super(TensorFlowModel, self).__init__()
        self.set_tensorflow_state(session=self.session, saver_state_file=self.saver_state_file, reload=True)

    def set_tensorflow_state(self, session=None, saver_state_file=None, reload=False):

        if session is not None:
            self.session = session

        if saver_state_file is not None:
            self.saver_state_file = saver_state_file

        if reload:
            self._load_tensorflow()

    def _load_tensorflow(self):
        self.session = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))

        if self.saver_state_file is not None:
            saver = tf.train.Saver()
            saver.restore(self.session, self.saver_state_file)
