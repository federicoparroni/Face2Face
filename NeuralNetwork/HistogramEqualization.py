from Augmentor.Operations import Operation
from skimage import exposure
from pylab import array, uint8
from PIL import Image
import numpy as np


class HistogramEqualization(Operation):

    def __init__(self, probability):
        Operation.__init__(self, probability)

    def perform_operation(self, image):
        image = exposure.equalize_adapthist(np.array(image[0]), clip_limit=0.01)
        image *= 255
        image = array(image, dtype=uint8)
        return [Image.fromarray(image)]
