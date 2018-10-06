import coremltools
import numpy
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
from keras.models import load_model

import os.path

input_name = 'finalmodel99.h5'
output_name = 'finalmodel99.mlmodel'

def convert_model(m):
    print('converting...')
    # coreml_model = coremltools.converters.keras.convert(m, input_names=['stacked_images'], image_input_names='stacked_images', class_labels=['different', 'same'])
    coreml_model = coremltools.converters.keras.convert(m)

    coreml_model.author = 'Parroni Federico'
    coreml_model.license = 'MIT'
    coreml_model.short_description = 'Predicts if two images contain two faces of the same person'
    #coreml_model.input_description['image'] = 'Two stacked 80x80 pixel images (2x80x80)'
    #coreml_model.output_description['output'] = 'Array with 2 values: first is probability of different people, second is probability of same person'
    coreml_model.save(output_name)
    print('model converted')


if os.path.isfile(input_name):
    model = load_model(input_name)
    convert_model(model)
else:
    print('no model found')
