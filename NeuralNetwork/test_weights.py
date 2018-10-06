import numpy as np
from ModelBuilder import read_model
import ModelBuilder
from keras.utils import np_utils
from LoadData import GetData
from keras.models import load_model


def print_weights(m):
    layers = m.layers
    for layer in layers:
        print(layer.get_weights())


def compare_weigths(m1, m2):
    layers1 = m1.layers
    layers2 = m2.layers
    if len(layers1) != len(layers2):
        return False
    else:
        for i in range(len(layers1)):
            w1 = layers1[i].get_weights()
            w2 = layers2[i].get_weights()
            if not np.array_equal(w1, w2):
                return False

        return True


# defining the folders path train and test
TRAINING_DATASET_FOLDER_NAME = '3_preprocessed_1_dataset train'

X_train, Y_train, _ = GetData(TRAINING_DATASET_FOLDER_NAME, limit_value=1)
Y_train = np_utils.to_categorical(Y_train, 2)
X_train = X_train.astype('float32')
X_train /= np.max(X_train)

width = 80
height = 80
depth = 2
num_classes = 2

# load the model architecture from file
a = read_model("models/model01.txt")
modelObject = ModelBuilder.ModelBuilder(a, (height, width, depth))
model = modelObject.model

model.compile(loss='categorical_crossentropy',  # using the cross-entropy loss function
              optimizer='adam',                 # using the Adam optimiser
              metrics=['accuracy'])             # reporting the accuracy

# train the model
model.fit(X_train, Y_train, batch_size=128, epochs=1, verbose=1, validation_split=0.2)

# print all the weights
# print_weights(model)

# save the model
model.save('prova_pesi.h5')

print("Model saved to file")
print("Im reloading the model from file...")

# load the saved model
# model.load_weights('my_model_weights.h5')
reloaded_model = load_model('prova_pesi.h5')

print("Weights are equals: ")
print(compare_weigths(model, reloaded_model))
