from common.abstract.machine_learning.model.tensorflow_.fastrcnn import TensorFlowFastRCNNModel

from common.utils.data_manipulation import get_maximum_value

from tffrcnn.networks import VGGnet_test

CLASSES = ('__background__',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')


class HumanPresenceClassifier(TensorFlowFastRCNNModel):

    network = VGGnet_test()

    def __init__(self, device=None):
        super(HumanPresenceClassifier, self).__init__()

    def classify(self, x_image):
        x_image_cv2_encoded = x_image.cv2_encode()
        object_proposals = self.detect_object_proposals(x_image_cv2_encoded)

        image_classifications = dict()

        for class_index, class_label in enumerate(CLASSES[1:]):
            class_index += 1  # due to skipping the __background__ class

            object_classifications = object_proposals.process_singular_class_index(class_index, label=class_label)
            image_classifications[class_label] = object_classifications

        return image_classifications

    @staticmethod
    def get_max_human_probability(image_classifications):
        return get_maximum_value(image_classifications['person'], lambda result: result.get_score())
