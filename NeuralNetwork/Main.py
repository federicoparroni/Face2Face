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

folders_at_the_same_time = 28
validation_folders = 14

validate_every = 2

batch_size = 128            # in each iteration, we consider 128 training examples at once
num_epochs = 300            # we iterate 200 times over the entire training set

height = 80
width = 80
depth = 2
num_classes = 2

# weight of the classes, when an error occour on class 0 -> false positive.
class_weight = {0: 1, 1: 1}

"""
================== TRAIN 1 SINGLE MODEL =====================

a = read_model("models/model9.txt")
modelObject = ModelBuilder.ModelBuilder(a, (height, width, depth))
model = modelObject.model

model.summary()

model.compile(loss='categorical_crossentropy',  # using the cross-entropy loss function
              optimizer='adam',                 # using the Adam optimiser
              metrics=['accuracy'])             # reporting the accuracy

# configuring training sequence
print("Loading {} validation folders...".format(validation_folders))

(X_validation, y_validation, validation_folders_list) = GetData(TRAINING_DATASET_FOLDER_NAME, limit_value=validation_folders)
X_validation = X_validation.astype('float32')
X_validation /= np.max(X_validation)    # Normalise data to [0, 1] range
Y_validation = np_utils.to_categorical(y_validation, num_classes)   # One-hot encode the labels

print("Starting training")
history = Train.SingletonTrain().Train(model, training_dataset_folder_name=TRAINING_DATASET_FOLDER_NAME,
                                       epochs=num_epochs, batch_size=batch_size,
                                       epochs_with_same_data=epochs_with_same_data,
                                       training_folders_count=folders_at_the_same_time, validation_x=X_validation,
                                       validation_y=Y_validation, to_avoid=validation_folders_list,
                                       validate_every=validate_every,
                                       early_stopping_after_epochs=3, early_stopping_margin=0.01,
                                       class_weight=class_weight, enable_telegram_bot=enable_telegram_bot)
"""

#=============== CROSS-VALIDATION =============

# LOAD THE MODELS TO CROSSVALIDATE

models_array, models_array_name = model_array_builder(
    sorted(['models/' + file for file in os.listdir('models')])
)

CrossValidate(
    1, models_array[6:], models_array_name[6:], TRAINING_DATASET_FOLDER_NAME, batch_size=batch_size, num_epochs=num_epochs,
    folders_at_the_same_time=folders_at_the_same_time, validate_every=validate_every, chat_id=chat_id,
    max_num_of_validation_folders=validation_folders
)
