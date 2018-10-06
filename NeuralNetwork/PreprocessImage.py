from AugmentationUtils import AugmentDataFromPath
from FaceExtractionPipeline import PreprocessImages
from Utils import convert_to_jpeg_recursive
from AugmentationUtils import FlipImagesRecursive

#============== AUGMENT THE DATASET =====================

#1 convert all the images pgm and png to jpeg
#convert_to_jpeg_recursive('/home/edoardo/Desktop/Dataset/1_dataset train')
#convert_to_jpeg_recursive('/home/edoardo/Desktop/Dataset/2_dataset test')

#2' flip images in the test(in the training is done automatically in the preprocessing)
#FlipImagesRecursive('/home/edoardo/Desktop/Dataset/2_dataset test')

#2 augment the data create new augmented photos in the folder
#AugmentDataFromPath('/home/edoardo/Desktop/Dataset/1_dataset train')

#3 crop the images augmented
PreprocessImages("/home/edoardo/Desktop/Dataset/1_dataset train")
#PreprocessImages("/home/edoardo/Desktop/Dataset/2_dataset test")