import os
import numpy as np
from LoadData import GetData
from keras.utils import np_utils
import Train
from Utils import current_datetime
from Utils import telegram_send_msg


def CrossValidate(k, models, models_array_name, dataset_folder_name, batch_size, num_epochs=200, chat_id="undefined",
                  folders_at_the_same_time=20, max_num_of_validation_folders=12, validate_every=5, validation_treshold=0):

    avg_val_accuracy_models = []
    total_num_folders = len(os.listdir(dataset_folder_name))
    folders_each_validation = total_num_folders // k if total_num_folders < max_num_of_validation_folders else max_num_of_validation_folders
    timestamp = current_datetime()
    path = 'Crossvalidation Results/crossvaliationresults_' + timestamp + '.txt'

    # folders where models will be saved
    os.mkdir("trained_model/" + timestamp)

    with open(path, 'w') as the_file:
        the_file.write(current_datetime() + '\n')

    for i in range(len(models)):
        print("\n validating model: " + models_array_name[i])
        sum_model_validations_acc = 0
        to_avoid_validation = []

        with open(path, 'a') as the_file:
            the_file.write('\n \n \n \n model: ' + str(i))

        with open(path, 'a') as the_file:
            models[i].summary(print_fn=lambda x: the_file.write('\n' + x + '\n'))

        # send a message on telegram when the training of another model is starting
        if chat_id != 'undefined':
            telegram_send_msg("START TRAINING {}".format(models_array_name[i]))

        for j in range(k):
            print("\n validation round " + str(j))
            (X_validation, Y_validation, validation_folders_list) = GetData(dataset_folder_name,
                                                                            limit_value=folders_each_validation)
            X_validation = X_validation.astype('float32')
            X_validation /= np.max(X_validation)
            Y_validation = np_utils.to_categorical(Y_validation, 2)
            to_avoid_validation = to_avoid_validation + validation_folders_list

            validation_history = Train.SingletonTrain().Train(
                models[i], training_dataset_folder_name=dataset_folder_name, epochs=num_epochs, batch_size=batch_size,
                training_folders_count=folders_at_the_same_time, validation_x= X_validation, validation_y=Y_validation,
                to_avoid=validation_folders_list, validate_every=validate_every, subfolder_name=timestamp,
                enable_telegram_bot=(chat_id != "undefined"), save_model=models_array_name[i], validation_treshold=validation_treshold
            )

            if len(validation_history) > 0:
                sum_model_validations_acc += (validation_history[-1])[1]

        avg_val_accuracy_models += [sum_model_validations_acc / k]

        with open(path, 'a') as the_file:
            the_file.write('\n validation results ' + str(sum_model_validations_acc / k))

