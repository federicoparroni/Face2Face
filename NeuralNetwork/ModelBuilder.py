from keras.models import Sequential
import keras
from keras.layers import Input, Convolution2D, MaxPooling2D, Dense, Dropout, Flatten, Activation


class ModelBuilder:

    """
    input for the method is a vector []
    in each position there is another vector with one of the following structure:
        'convolution', conv_depth, conv_depth kernel_size, activation
        'pooling', pool_size, pool_size
        'dropout', dropout_probability
        'flatten'
        'dense', hidden_size, activation
    """

    def __init__(self, model_structure, input_shape):
        model = Sequential()
        for i in range(0, len(model_structure)):
            ms = model_structure[i]
            if ms[0] == 'conv':
                if i == 0:
                    if len(ms) == 5:
                        model.add(Convolution2D(ms[1], (ms[2], ms[3]), activation=ms[4], padding='same', input_shape=input_shape))
                    else:
                        model.add(Convolution2D(ms[1], (ms[2], ms[3]), activation='relu', padding='same', input_shape=input_shape))
                else:
                    if len(ms) == 5:
                        model.add(Convolution2D(ms[1], (ms[2], ms[3]), activation=ms[4], padding='same'))
                    else:
                        model.add(Convolution2D(ms[1], (ms[2], ms[3]), activation='relu', padding='same'))
            elif ms[0] == 'pool':
                model.add(MaxPooling2D(pool_size=(ms[1], ms[2])))
            elif ms[0] == 'dropout':
                model.add(Dropout(ms[1]))
            elif ms[0] == 'flatten':
                model.add(Flatten())
            elif ms[0] == 'dense':
                if len(ms) == 3:
                    model.add(Dense(ms[1], activation=ms[2]))
                else:
                    model.add(Dense(ms[1], activation='relu'))
        self.model = model


def read_model(filepath):
    out = []

    with open(filepath) as file:
        for line in file.readlines():
            line = line.strip()
            if line and not line.startswith("#"):
                fields = line.split(",")
                # cast
                v = [fields[0]]
                for i in range(1, len(fields)):
                    if v[0] == "dropout":
                        v.append(float(fields[i]))
                    elif v[0] == 'dense' and i == 2:
                        v.append(fields[i])
                    else:
                        v.append(int(fields[i]))

                out.append(v)
    return out

"""
#a = [['conv', 16, 3, 3], ['pool', 3, 3], ['flatten'], ['dense', 128], ['dense', 128]]
a = ModelBuilder.read_model("models/model1.txt")
size = (80, 80, 2)
modelObject = ModelBuilder(a, size)
print(modelObject.model.summary())
"""


def model_array_builder(filepath_array):
    models_array = []
    models_name_array = []

    for i in filepath_array:
        a = read_model(i)
        modelObject = ModelBuilder(a, (80, 80, 2))
        model = modelObject.model

        model.compile(loss='categorical_crossentropy',  # using the cross-entropy loss function
                      optimizer=keras.optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0),
                      metrics=['accuracy'])

        models_array.append(model)
        models_name_array.append(i.split('/')[-1])
        del modelObject
        del model

    return models_array, models_name_array
