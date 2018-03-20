from abc import ABCMeta, abstractmethod

from common.abstract.machine_learning.model.caffe_ import CaffeModel

import numpy as np
import caffe
import copy
import os

class CaffeNetworkModel(CaffeModel):

    __metaclass__ = ABCMeta

    network_file = None
    weights_file = None
    mean = None

    _network = None
    _transformer = None

    def __init__(self, device=None):
        super(CaffeNetworkModel, self).__init__(device=device)
        self.set_caffe_network(network_file=self.network_file, weights_file=self.weights_file, mean=self.mean, reload=True)

    def set_caffe_network(self, network_file=None, weights_file=None, mean=None, reload=False):

        if network_file is not None:
            self.network_file = network_file

        if weights_file is not None:
            self.weights_file = weights_file

        if mean is not None:
            self.mean = mean

        if reload:
            self._load_caffe_network()

    def _load_caffe_network(self):
        self._network = caffe.Net(self.network_file, self.weights_file, caffe.TEST)
        self._transformer = caffe.io.Transformer({'data': self._network.blobs['data'].data.shape})
        mean = self._load_mean_array(self.mean)
        self._transformer.set_mean('data', mean)

    def _load_mean_array(self, mean):
        if type(mean) is np.array:
            return mean

        if not os.path.isfile(mean):
            raise ImportError('CaffeNetwork mean parameter is not valid.')

        filename, file_extension = os.path.splitext(mean)
        file_extension_to_lower = file_extension.lower()

        if file_extension_to_lower == '.npy':
            return np.load(mean).mean(1).mean(1)

        elif file_extension_to_lower == '.binaryproto':
            mean_blob = caffe.proto.caffe_pb2.BlobProto()

            with open(mean) as f:
                mean_blob.ParseFromString(f.read())

            mean_array = np.asarray(mean_blob.data, dtype=np.float32).reshape(
                (mean_blob.channels, mean_blob.height, mean_blob.width))[0,:,:]
            mu0, mu1, mu2 = np.mean(mean_array[0]), np.mean(mean_array[1]), np.mean(mean_array[2])
            return np.array([mu0, mu1, mu2])

        raise ImportError('CaffeNetwork mean parameter could not find a matching pre-processor.')

    def _network_feed_forward(self, x_transform):
        """
        _network_feed_forward() takes in compatible data and places it in the input layer
        of our neural network.

        _network.forward() runs the input data through the network and our output layer
        is typically placed under blobs['conv'] or blobs['prob']
        :param X_transform: pre-processed data that is compatible with our network.
        :return: CaffeNetworkFeedForwardState(network, output)
        """
        self._network.blobs['data'].data[...] = x_transform
        network_output = self._network.forward()

        return CaffeNetworkFeedForwardState(self._network, network_output)

    @abstractmethod
    def predict(self, x):
        pass


class CaffeNetworkFeedForwardState:

    def __init__(self, network, output):
        self.network_blobs = self.copy_network_blobs(network.blobs)
        self.output = copy.deepcopy(output)

    def get_output(self):
        return self.output

    def get_network_blobs(self):
        return self.network_blobs

    def get_network_params(self):
        return self.network_params

    def copy_network_blobs(self, blobs):
        saved_data = dict()

        for layer_name, blob in blobs.iteritems():
            saved_data[layer_name] = dict()
            saved_data[layer_name]['data'] = np.array(blob.data)

        return saved_data
