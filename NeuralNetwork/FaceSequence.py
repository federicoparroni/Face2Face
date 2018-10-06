import keras
import numpy as np
import LoadData
from keras.utils import np_utils
import math
import threading
import gc

from Utils import current_datetime
import telegram


class FaceSequence(keras.utils.Sequence):

    def __init__(self, batch_size, training_dataset_folder_name, total_epochs, epochs_with_same_data=5,
                 folders_at_the_same_time=20, to_avoid=[], enable_telegram_bot=True, chat_id="undefined"):
        self.x, self.y, _ = LoadData.GetData(training_dataset_folder_name,
                                             limit_value=folders_at_the_same_time,
                                             to_avoid=to_avoid)
        self.y = np_utils.to_categorical(self.y, 2)
        self.x = self.x.astype('float32')
        self.x /= np.max(self.x)

        self.x_next_epoch, self.y_next_epoch = self.x, self.y
        self.epoch = 0
        self.batch_size = batch_size
        self.epochs_with_same_data = epochs_with_same_data
        self.training_dataset_folder_name = training_dataset_folder_name
        self.folders_at_the_same_time = folders_at_the_same_time
        self.to_avoid = to_avoid
        self.steps_per_epoch = 0
        self.t = None
        self.total_epochs = total_epochs
        self.enable_telegram_bot = enable_telegram_bot
        self.chat_id = chat_id

    def __len__(self):
        self.steps_per_epoch = int(np.ceil(len(self.x) / float(self.batch_size)))
        return self.steps_per_epoch

    def __getitem__(self, idx):
        batch_x = self.x[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.y[idx * self.batch_size:(idx + 1) * self.batch_size]
        return np.array(batch_x), np.array(batch_y)

    def on_epoch_end(self):
        if self.enable_telegram_bot:
            bot = telegram.Bot(token='591311395:AAEfSH464BdXSDezWGMZwdiLxLg2_aLlGDE')
            message = "{} - Ho completato l'epoca {}".format(current_datetime(), self.epoch)
            bot.send_message(chat_id=self.chat_id, text=message, timeout=100)

        try:
            gc.collect()
            if self.epoch % self.epochs_with_same_data == 0:
                if self.t != None:
                    self.t.join()
                self.x = self.x_next_epoch
                self.y = self.y_next_epoch
                self.batch_size = math.floor(len(self.x) / self.steps_per_epoch)
            else:
                s = np.arange(self.x.shape[0])
                np.random.shuffle(s)
                self.x = self.x[s]
                self.y = self.y[s]
        except Exception as error:
            bot = telegram.Bot(token='591311395:AAEfSH464BdXSDezWGMZwdiLxLg2_aLlGDE')
            message = "{} - Sono schiantato malamente :/\n{}".format(current_datetime(), error)
            bot.send_message(chat_id=self.chat_id, text=message, timeout=100)

    def on_epoch_begin(self):
        if self.epoch % self.epochs_with_same_data == 0:
            if self.epoch + self.epochs_with_same_data != self.total_epochs:
                if self.t != None:
                    self.t.join()
                self.t = threading.Thread(target=self.fetch_data_for_next_couple_of_epochs, args=())
                self.t.setDaemon(True)
                self.t.start()
        self.epoch += 1

    def fetch_data_for_next_couple_of_epochs(self):
        self.x_next_epoch, self.y_next_epoch, _ = LoadData.GetData(self.training_dataset_folder_name,
                                                  limit_value=self.folders_at_the_same_time, to_avoid=self.to_avoid)
        self.y_next_epoch = np_utils.to_categorical(self.y_next_epoch, 2)
        self.x_next_epoch = self.x_next_epoch.astype('float32')
        self.x_next_epoch /= np.max(self.x_next_epoch)
