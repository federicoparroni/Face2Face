from Augmentor.Operations import Operation
from pylab import array, uint8
from PIL import Image
import numpy as np
import random


class AlterBrightness(Operation):

    count = 0
    phi = 1
    theta = 1
    maxIntensity = 255
    lowerBoundA = 0.4
    upperBoundA = 1
    lowerBoundB = 1
    upperBoundB = 2.5

    def __init__(self, probability):
        Operation.__init__(self, probability)
        self.count = 0

    def perform_operation(self, image):
        if self.count % 2 == 0:
            image = (self.maxIntensity / self.phi) * (np.array(image[0]) / (self.maxIntensity / self.theta)) ** (random.random()*(self.upperBoundA-self.lowerBoundA)+self.lowerBoundA)
        else:
            image = (self.maxIntensity / self.phi) * (np.array(image[0]) / (self.maxIntensity / self.theta)) ** (random.random()*(self.upperBoundB-self.lowerBoundB)+self.lowerBoundB)
        image = array(image, dtype=uint8)
        self.count += 1
        return [Image.fromarray(image)]
