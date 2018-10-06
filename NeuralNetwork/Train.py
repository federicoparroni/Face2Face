from Utils import current_datetime
import keras
import numpy as np
import LoadData
import threading
from keras.utils import np_utils
from Utils import telegram_send_msg
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = "591311395:AAEfSH464BdXSDezWGMZwdiLxLg2_aLlGDE"

_instances = {}


class SingletonTrain(object):

    def __new__(cls, *args, **kw):
        if cls not in _instances:
            instance = super().__new__(cls)
            instance.stop_training = False
            _instances[cls] = instance

        return _instances[cls]

    def _stop_training(self):
        self.stop_training = True

    def Train_Sequence(self, model, train_sequence, num_epochs=200, chat_id="undefined", training_callbacks=[], save_model=True):
        if chat_id != "undefined":
            telegram_send_msg("Training iniziato...")

        model.fit_generator(train_sequence, epochs=num_epochs, callbacks=[keras.callbacks.LambdaCallback(
                            on_epoch_begin=lambda batch, logs: train_sequence.on_epoch_begin())]+training_callbacks)

        if chat_id != "undefined":
            telegram_send_msg("Training completato!")

        # ONLY WHEN U WANT USE THE TEST SET!!!
        # WARNING ONLY WHEN WE WANT THE TEST ERROR CAN BE DONE ONLY ONE TIME!
        # loss = model.evaluate(X_test, Y_test, verbose=1)  # Evaluate the trained model on the test set!

        # ====== save model ======
        # the three following instructions must be decommented when we want to save the model at the end of the training
        if chat_id != "undefined" and save_model:
            telegram_send_msg("Sto salvando il modello")

        if save_model:
            model.save('trained_model/{}.h5'.format(current_datetime()))

        if chat_id != "undefined" and save_model:
            telegram_send_msg("{} - Modello salvato!")

    y_next_epoch = []
    x_next_epoch = []

    def Train(self, model, training_dataset_folder_name, epochs, batch_size, training_folders_count, validation_x,
              validation_y, to_avoid, validate_every, early_stopping_after_epochs=0, early_stopping_margin=1,
              validation_treshold=0, class_weight={0: 1, 1: 1}, enable_telegram_bot=False, save_model=None, subfolder_name=None):

        # telegram bot init
        updater = Updater(token=BOT_TOKEN)
        dispatcher = updater.dispatcher
        interrupt_handler = CommandHandler('next_model', lambda b, u: self._stop_training())
        dispatcher.add_handler(interrupt_handler)
        updater.start_polling()

        load_new_data = True
        t = None
        validation_history = []
        epochs_performed = 0
        EPOCHS_WITH_SAME_DATA = 3

        # load training data
        x, y, _ = self.load_data(folders=training_dataset_folder_name, folders_to_load=training_folders_count,
                                 to_avoid=to_avoid)

        # train the model for the number of epochs specified
        for current_epoch in range(epochs):

            # insert an interrupt in the training with a telegram message
            if self.stop_training:
                self.stop_training = False
                t.join()
                break


            if load_new_data:
                load_new_data = False

                t = threading.Thread(target=self.load_data, args=(training_dataset_folder_name, training_folders_count,
                                                                  to_avoid))
                t.setDaemon(True)
                t.start()

            print("\nEpoch {}/{}".format(current_epoch+1, epochs))

            last_epoch_result = model.fit(x, y, batch_size=batch_size, epochs=1, verbose=1,
                                          class_weight=class_weight, callbacks=None, shuffle=True)

            epochs_performed += 1
            last_pos = len(last_epoch_result.history['acc'])
            last_epoch_acc = last_epoch_result.history['acc'][last_pos-1]

            # ============= VALIDATION =============
            # perform validation every "validate_every" epochs

            if (current_epoch+1) % validate_every == 0:
                evaluation = model.evaluate(validation_x, validation_y)
                print(evaluation)
                print("training_accuracy: {}".format(last_epoch_acc))
                validation_history.append(evaluation)
                if enable_telegram_bot:
                    telegram_send_msg("Ho completato l'epoca {}\n{}\nValidation loss: {}, \n "
                                      "validation_accuracy: {}, \n\n training_accuracy: {}"
                                      .format(current_epoch+1, "-"*15, evaluation[0], evaluation[1], last_epoch_acc))

                if 0 < early_stopping_after_epochs < len(validation_history):
                    current_val_accuracy = evaluation[1]
                    should_terminate = True
                    for e in validation_history:
                        if current_val_accuracy > e[1] - early_stopping_margin:
                            should_terminate = False

                    if should_terminate:
                        print("~~~~~~~~~~~~~ Early-stopping occurred! Last {} validation accuracies: "
                              .format(early_stopping_after_epochs))
                        [print(h[1]) for h in validation_history[-early_stopping_after_epochs-1:]]
                        print("~~~~~~~~~~~~~")
                        return validation_history

            # change tha training dataset when the validation accuracy decrease
            # validation_history_len = len(validation_history)
            # if validation_history_len > 1 and epochs_performed > 1:
            #     if validation_history[validation_history_len - 2][1] - \
            #             validation_history[validation_history_len - 1][1] > validation_treshold:

            #CHANGE DATA EVERY EPOCHS_WITH_SAME_DATA epochs
            if epochs_performed % EPOCHS_WITH_SAME_DATA == 0:

                t.join()
                load_new_data = True
                # send a message when the data are changing
                if enable_telegram_bot:
                    telegram_send_msg("Changing data")

                epochs_performed = 0

                x = self.x_next_epoch
                y = self.y_next_epoch

            # ============= end validation

            if enable_telegram_bot and (current_epoch+1) % validate_every != 0:
                telegram_send_msg("Ho completato l'epoca {} \n accuracy: {}".format(current_epoch+1, last_epoch_acc))

        if save_model is not None:
            if subfolder_name is None:
                model.save('trained_model/{}_{}.h5'.format(save_model, current_datetime()))
            else:
                model.save('trained_model/{}/{}_{}.h5'.format(subfolder_name, save_model, current_datetime()))

        return validation_history

    def load_data(self, folders, folders_to_load=15, to_avoid=[]):
        # print("\nstarted the fetch of data for the next epoch in parallel")
        self.x_next_epoch, self.y_next_epoch, loaded_folders_list = LoadData.GetData(folders, limit_value=folders_to_load,
                                                                                     to_avoid=to_avoid)
        self.y_next_epoch = np_utils.to_categorical(self.y_next_epoch, 2)
        self.x_next_epoch = self.x_next_epoch.astype('float32')
        self.x_next_epoch /= np.max(self.x_next_epoch)
        # print("\nended the fetch of data for the next epoch in parallel")
        return self.x_next_epoch, self.y_next_epoch, loaded_folders_list
