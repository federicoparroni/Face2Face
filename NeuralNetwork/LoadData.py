from skimage import io
from random import shuffle
import skimage
import numpy as np
import os
import math
import random


def LoadData(folder_path, limit_value=-1, to_avoid=[]):
    img_data_list = []  # elements list, an element is a couple of image (i1,i2)
    img_label_list = []  # labels list, can be 1 if the faces are the same or 0 if not
    folders_list = []
    count = 0

    # load images from the preprocessed folder
    folders = os.listdir(folder_path)
    random.shuffle(folders)

    for i in folders:
        if not(len(to_avoid) > 0 and i in to_avoid):
            print('\n{}/{} fetching data from {}/{}'.format(count, limit_value, folder_path, i))
            a, b = CreatePositiveCouples(folder_path + '/' + i)
            c, d = CreateNegativeCouples(folder_path + '/' + i)

            # print(len(a))
            # print(len(c))

            folders_list.append(i)

            for j in range(len(a)):
                img_data_list.append(a[j])
                img_label_list.append(b[j])

            for j in range(len(c)):
                img_data_list.append(c[j])
                img_label_list.append(d[j])

            count += 1
            if limit_value != -1 and count >= limit_value:
                break

    return img_data_list, img_label_list, folders_list


# creates the couples for which the correspondence of the face is true (same person)
def CreatePositiveCouples(folder_path):
    img_data_list = []              # elements list, an element is a couple of image (i1,i2)
    img_label_list = []             # labels list, can be 1 if the faces are the same or 0 if not

    for img1 in os.listdir(folder_path):
        for img2 in os.listdir(folder_path):
            #no consider the same image when creating positive couple
            #if img1 != img2:
            couple = CreateCouple(folder_path + '/' + img1, folder_path + '/' + img2)
            if couple is not None:
                img_data_list.append(couple)
                img_label_list.append(1)

    return img_data_list, img_label_list


# creates the couples for which the correspondence of the face is false(different person)
def CreateNegativeCouples(folder_path):
    img_data_list = []              # elements list, an element is a couple of image (i1,i2)
    img_label_list = []             # labels list, can be 1 if the faces are the same or 0 if not

    couples_to_do = len(os.listdir(folder_path))

    for img1 in os.listdir(folder_path):
        folders = os.listdir(folder_path + '/..')

        basePath = folder_path.split('/')[0]
        # remove the name of the current folder
        folders.remove(folder_path.split('/')[-1:][0])

        for i in range(couples_to_do):
            shuffle(folders)
            i = basePath + '/' + folders[0]

            rnd_numb = math.floor(random.random() * len(os.listdir(i)))
            img2 = i + '/' + os.listdir(i)[rnd_numb]

            couple = CreateCouple(folder_path + '/' + img1, img2)
            if couple is not None:
                img_data_list.append(couple)
                img_label_list.append(0)

    return img_data_list, img_label_list


# return the concatenation of the two images after the preprocessing
def CreateCouple(img1_path, img2_path):
    # read preprocessed images
    input_img1 = skimage.io.imread(img1_path)
    input_img2 = skimage.io.imread(img2_path)

    # bring images in grayscale
    # input_img1 = skimage.color.rgb2gray(input_img1)
    # input_img2 = skimage.color.rgb2gray(input_img2)

    # resize of the image
    # r_input_img1 = resize(input_img1, (input_img1.shape[0]//2, input_img1.shape[1]//2))
    # r_input_img2 = resize(input_img2, (input_img2.shape[0]//2, input_img2.shape[1]//2))

    # concatenate the two arrays
    # inp = np.concatenate((input_img1, input_img2))

    return MergeImages(input_img1, input_img2)


def MergeImages(img1, img2):
    # return np.concatenate((img1, img2))
    return np.stack((img1, img2), 2)

# set the attributes to some values if we dont like to fetch all the folders starting from a path
# as a conseguence, also the attributes of load data will be set to the same values
def GetData(path, limit_value = -1, to_avoid = []):
    (img_data_list, img_label_list, folders_list) = LoadData(path, limit_value, to_avoid)

    v = list(range(len(img_label_list)))
    shuffle(v)

    vec = []
    label_vec = []

    for i in range((len(v))):
        vec.append(img_data_list[v[i]])
        label_vec.append(img_label_list[v[i]])

    # when the images were concatenated one near the other
    # return np.expand_dims(np.array(vec), 4), np.array(label_vec)

    # the images are stacked one over the other
    np_vec = np.array(vec)
    np_label_vec = np.array(label_vec)

    # print('dim of loaded vect' + np_vec.shape)

    return np_vec, np_label_vec, folders_list


# print for a vector of extimation if they are correct
def ResultPrediction(extimation, real_label):
    str_extimation = np.array2string(extimation, None, 4)
    str_real_label = np.array2string(real_label, None, 4)
    if real_label[0] == 1:
        if extimation[0] > 0.5:
            return 'OK' + ': ' + str_extimation         # + ' \n r_l ' + str_real_label
        else:
            return 'E' + ': ' + str_extimation          # + ' \n r_l ' + str_real_label
    else:
        if extimation[1] > 0.5:
            return 'OK' + ': ' + str_extimation         # + ' \n r_l ' + str_real_label
        else:
            return 'E' + ': ' + str_extimation          # + ' \n r_l ' + str_real_label

