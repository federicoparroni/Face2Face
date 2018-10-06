import tensorflow as tf
import Train
import numpy as np
from ModelBuilder import read_model
import ModelBuilder
from Utils import connection_available
from keras.utils import np_utils
from LoadData import GetData
from ModelBuilder import model_array_builder
from KFoldCrossValidation import CrossValidate
import os

import keras
from Utils import current_datetime
from ModelBuilder import read_model
from ModelBuilder import ModelBuilder
from keras.utils.vis_utils import plot_model

from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import seaborn as sn
import pandas as pd
import itertools
from sklearn import metrics
from math import ceil

# ====================CONFIGURING GPU ========================================
config = tf.ConfigProto()
config.gpu_options.allow_growth = False

# ============================================================================

enable_telegram_bot = True if connection_available() else False
# chat_id = 125016709               # this is my private chat id
# chat_id = "@gdptensorboard"       # this is the name of the public channel
chat_id = -1001223624517            # this is for the private channel

# defining the folders path train and test
TRAINING_DATASET_FOLDER_NAME = '3_preprocessed_1_dataset train'
TEST_DATASET_FOLDER_NAME = '3_preprocessed_2_dataset test'

epochs_with_same_data = 10
folders_at_the_same_time = 25
validation_folders = 1
validate_every = 2

batch_size = 128            # in each iteration, we consider 128 training examples at once
num_epochs = 1            # we iterate 200 times over the entire training set

height = 80
width = 80
depth = 2
num_classes = 2

def vect_to_1D(vector,threshold):
    predictions_1D = []
    for i in vector:
        if i[1] > threshold:
            predictions_1D.append(1)
        else:
            predictions_1D.append(0)
    return predictions_1D


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')




a = read_model("models/model08.txt")
modelObject = ModelBuilder(a, (80, 80, 2))
model = modelObject.model
model.load_weights('trained_model/2018-07-04 22:29:20/model08.txt_2018-07-05 12:24:21.h5')
#plot_model(model, to_file='model_graph.png', show_shapes=True, show_layer_names=True)

(X_test, y_test, _) = GetData('lfw-whofitinram_p80x80')
Y_test = np_utils.to_categorical(y_test, num_classes)
X_test = X_test.astype('float32')
X_test /= np.max(X_test)    # Normalise data to [0, 1] range
model.compile(loss='categorical_crossentropy',  # using the cross-entropy loss function
              optimizer='adam',                 # using the Adam optimiser
              metrics=['accuracy'])

model.summary()
#evaluate the mode
print(model.evaluate(X_test, Y_test))
predictions = model.predict(X_test)

#========================PRINT CONFUSION MATRIX==============================
#predict labels

predictions_1D = vect_to_1D(predictions,0.8)
real_label_1D = vect_to_1D(Y_test,0.8)

cm1 = sklearn.metrics.confusion_matrix(vect_to_1D(predictions, 0.9), vect_to_1D(Y_test, 0.9))
cm2 = sklearn.metrics.confusion_matrix(vect_to_1D(predictions, 0.5), vect_to_1D(Y_test, 0.5))

np.set_printoptions(precision=2)
plt.figure()
plot_confusion_matrix(cm1, classes=[1, 0], normalize=True,
                      title='Confusion matrix')
plt.show()
plot_confusion_matrix(cm2, classes=[1, 0], normalize=True,
                      title='Confusion matrix')
plt.show()

#==========================================================================

# calculate the fpr and tpr for all thresholds of the classification
probs = model.predict_proba(X_test)
preds = predictions[:, 1]
fpr, tpr, threshold = metrics.roc_curve(y_test, preds)
roc_auc = metrics.auc(fpr, tpr)

"""
fpr_discrete = []
tpr_discrete = []
threshold_discrete = []

for i in range(len(threshold)):
    if i%1000 == 0:
        fpr_discrete.append(fpr[i])
        tpr_discrete.append(tpr[i])
        threshold_discrete.append(threshold[i])
"""


# method I: plt
plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.grid
plt.show()




