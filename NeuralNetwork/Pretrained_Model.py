from LoadData import GetData
from LoadData import ResultPrediction

from PlotImage import plot

from keras.utils import np_utils
from keras.models import load_model
import numpy as np
import ModelBuilder
from ModelBuilder import read_model


#===================================

bp = 'trained_model/'

NUM_CLASSES = 2
TEST_DATASET_FOLDER_NAME ='3_preprocessed_1_dataset train'
MAX_IMAGES_TO_PLOT = 36
NUM_PRINTED_PAGES = 3
MODEL_TO_LOAD = '2018-05-06 15:25:00.h5'

a = read_model("models/model1.txt")
modelObject = ModelBuilder.ModelBuilder(a, (80, 80, 2))
model = modelObject.model
model.load_weights(bp + MODEL_TO_LOAD)

#model = load_model(bp + MODEL_TO_LOAD)

(X_test, y_test, _) = GetData(TEST_DATASET_FOLDER_NAME, 5)
Y_test = np_utils.to_categorical(y_test, NUM_CLASSES)
X_test = X_test.astype('float32')
X_test /= np.max(X_test)    # Normalise data to [0, 1] range
model.compile(loss='categorical_crossentropy',  # using the cross-entropy loss function
              optimizer='adam',                 # using the Adam optimiser
              metrics=['accuracy'])

print(model.evaluate(X_test, Y_test))

sum = 0
for i in range(len(y_test)):
    sum += y_test[i]

print(sum)
print(len(y_test))

predicted_label = model.predict(X_test)

# creates titles to plot the predicted classes
titles = []
X_test_concatenated = []
for i in range(len(X_test)):
    result = predicted_label[i]
    real_value = Y_test[i]
    # plt.imshow(np.squeeze(X_test[i], axis=2), 'gray')
    if result[1] > 0.9 and real_value[1] == 0:
        titles.append(ResultPrediction(result, real_value))
        X_test_concatenated.append(np.concatenate((np.array(X_test[i, :, :, 0]), np.array(X_test[i, :, :, 1]))))

# show the images in plots
for k in range(NUM_PRINTED_PAGES):
    _from = k*MAX_IMAGES_TO_PLOT
    _to = (k+1)*MAX_IMAGES_TO_PLOT
    plot(X_test_concatenated[_from:_to], titles[_from:_to], MAX_IMAGES_TO_PLOT)
