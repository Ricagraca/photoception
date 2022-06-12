
from email.mime import image
import imageio
import scipy as scipy
import os.path
from os import path

from CalculateImageOutOfVideo import CalculateImageOutOfVideo
from CompareAverage import CompareAverage

IMAGE_FOLDER = 'image/'
VIDEO_FOLDER = 'video/'
SAVED_FOLDER = 'saved/'


def create(image_file, video_file, frame_number, factorx=10, factory=10, output=None):

    image_calculator = CalculateImageOutOfVideo(VIDEO_FOLDER + video_file, frame_number, well_divided=True)
    image = imageio.imread(IMAGE_FOLDER + image_file, pilmode='RGB')
    image_calculator.calculate_image(image,CompareAverage(), factorx, factory)
    image_calculator.save_image(SAVED_FOLDER + 'saved_' + (output if output is not None else image_file))


def create_several(image_file, video_file, frame_number, number_images):

    file_name_without_extension = image_file.split(".")[0]
    extension = image_file.split(".")[1]
    saving_directory = SAVED_FOLDER + file_name_without_extension + '/'

    height = 256
    width = 256

    image_calculator = CalculateImageOutOfVideo(VIDEO_FOLDER + video_file, frame_number, well_divided=True)
    image = imageio.imread(IMAGE_FOLDER + image_file, pilmode='RGB')
    
    if not path.exists(saving_directory):
        os.mkdir(saving_directory)

    for i in range(1,number_images+1):
        saved_file_name = file_name_without_extension + str(i) + '.' + extension
        if path.exists(saving_directory + saved_file_name):
            print("File " + saving_directory + saved_file_name + " exists.")
            continue

        factory_, factorx_ = height//(i), width//(i)
        image_calculator.calculate_image(image,CompareAverage(), factorx_, factory_)
        image_calculator.save_image(saving_directory + saved_file_name)


if __name__ == '__main__':

    image_file = 'dwight.jpg'
    video_file = 'video.mp4'
    frame_number = 100
    number_of_images = 64

    create_several(image_file, video_file, frame_number, number_of_images)