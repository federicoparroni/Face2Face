import Augmentor
import os
import AlterBrightness
import HistogramEqualization
from Utils import convert_to_jpg
from PIL import Image, ExifTags
from FaceExtractionPipeline import PreprocessImages


def AugmentDataFromPath(path):
    #rotate the images in vertical positions
    FlipImages(path)

    #augementation part of the code
    entries = os.scandir(path)
    alter_brightness = AlterBrightness.AlterBrightness(1)
    histogram_equalization = HistogramEqualization.HistogramEqualization(0.5)
    p = Augmentor.Pipeline(path, output_directory='.')
    p.flip_left_right(probability=0.5)
    p.skew_left_right(probability=1, magnitude=0.20)
    p.add_operation(alter_brightness)
    p.add_operation(histogram_equalization)

    for entry in entries:
        if entry.is_dir():
            AugmentDataFromPath(entry.path)
        else:
            #convert the image to jpg
            convert_to_jpg(entry.path)

            p.sample((6*len([name for name in entries])+1))
            break

def FlipImages(path):
    entries = os.scandir(path)
    for entry in entries:
        if not entry.is_dir():
            try:
                image=Image.open(entry.path)
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image._getexif().items())

                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                    print(entry.path)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                    print(entry.path)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
                    print(entry.path)
                image.save(entry.path)
                image.close()

            except (AttributeError, KeyError, IndexError):
                # cases: image don't have getexif
                pass



def FlipImagesRecursive(path):
    entries = os.scandir(path)
    for entry in entries:
        if not entry.is_dir():
            FlipImages(path)
        else:
            FlipImagesRecursive(entry.path)

