import dlib
import matplotlib.pyplot as plt
import os
from face_utils import FaceAligner
import skimage.io
import numpy as np

# path of the preprocessed dataset
PREPROCESSED_IMAGES_FOLDER_PATH = "3_preprocessed_"
_instances = {}

face_detector = None
predictor = None
fa = None

class SingletonPipeline(object):

    def __new__(cls, *args, **kw):
        if not cls in _instances:
            instance = super().__new__(cls)
            _instances[cls] = instance

            instance.face_detector = dlib.get_frontal_face_detector()
            instance.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
            instance.fa = FaceAligner(instance.predictor, desiredFaceWidth=80)

        return _instances[cls]

    # applies the face extraction pipeline to a single image
    #
    # REQUIRES: a general image, whatever RGB or GrayScale, in any resolution and acquired from any library. other than
    # this. also two cutmargins that can be applied to crop the image in width and height can be provided
    #
    # RETURNS: the extracted face from the image, cropped and with the eyes aligned, if any
    def FaceExtractionPipelineImage(self, image, cut_margin_width=0, cut_margin_heigth=0):
        # start_time = time.time()

        # if we'd like to perform a precut we do it here
        if cut_margin_width != 0 or cut_margin_heigth != 0:
            image = self.CropBorders(image, cut_margin_width, cut_margin_heigth)

        # Run the HOG face detector on the image data. The result will be the bounding boxes of the faces in our image.
        detected_faces = self.face_detector(image, 1)

        # Bypass, if more then one face is found I just reject the face
        if len(detected_faces) == 1:

            # Loop through each face we found in the image
            for i, face_rect in enumerate(detected_faces):

                face_aligned = self.fa.align(image, image, face_rect)

                if len(face_aligned.shape) == 3:
                    face_aligned = skimage.color.rgb2gray(face_aligned)
                    face_aligned = face_aligned*255
                    face_aligned = face_aligned.astype('int')

                # print('----- execution time for the pipeline: ', time.time() - start_time)
                face_aligned = face_aligned.astype('float32')
                face_aligned /= np.max(face_aligned)
                return face_aligned


    def CropBorders(self, image, cut_margin_width, cut_margin_heigth):
        image = np.array(image)
        first_dim = image.shape[0]
        second_dim = image.shape[1]
        cropped_image = image[cut_margin_width:first_dim - cut_margin_width,
                        cut_margin_heigth:second_dim - cut_margin_heigth, :]
        return cropped_image


# outputs the results of the pipeline to all the images starting from the dataset_root_path
def TryThePipeline(dataset_root_path):
    folders = os.listdir(dataset_root_path)

    for i in folders: # scan all the images of that folder
        im = skimage.io.imread(dataset_root_path + '/' + i)
        img = SingletonPipeline().FaceExtractionPipelineImage(im)
        if img is not None:
            print(dataset_root_path + '/' + i)
            plt.imshow(img, 'gray')
            plt.show()
        else:
            print('error in: ' + dataset_root_path + '/' + i)

# TryThePipeline('/home/giovanni/Immagini/Webcam')

# ==========PREPROCESSING load data ================

def PreprocessImages(folder):
    # preproc_folder = PREPROCESSED_IMAGES_FOLDER_PATH + folder
    preproc_folder = folder
    if not os.path.isdir(preproc_folder + '_p'):
        os.mkdir(preproc_folder + '_p')

    for f in os.listdir(folder):
        if not os.path.isdir(preproc_folder + '_p'+ "/" + f):
            os.mkdir(preproc_folder + '_p' + "/" + f)
            for img in os.listdir(folder + "/" + f):
                image = skimage.io.imread(folder + "/" + f + '/' + img)
                preproc_img = SingletonPipeline().FaceExtractionPipelineImage(image)

                if preproc_img is not None:
                    skimage.io.imsave(preproc_folder + '_p'+ "/" + f + '/' + img, preproc_img)
                    print("Created: " + preproc_folder + '_p' + "/" + f + '/' + img)
                else:
                    print("Image null: " + preproc_folder + '_p' + "/" + f + '/' + img)
    #else:
    #    print("Folder already created. Delete the old one and retry.")

