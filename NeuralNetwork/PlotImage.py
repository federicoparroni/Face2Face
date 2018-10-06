import numpy as np
import math
import matplotlib.pyplot as plt


def plot(images, labels, count):
    fig = plt.figure()

    for i in range(count):
        a = fig.add_subplot(math.ceil(count ** .5), math.ceil(count ** .5), i+1)
        plt.imshow(images[i], 'gray')
        a.set_title(labels[i])
        a.axis('off')

    plt.show()
