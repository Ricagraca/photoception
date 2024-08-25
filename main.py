from email.mime import image
import imageio
import scipy as scipy
import os.path
import cv2
from os import path

from CalculateImageOutOfVideo import CalculateImageOutOfVideo, number_of_frames, video_porportion
from CompareAverage import CompareAverage

IMAGE_FOLDER = 'image/'
VIDEO_FOLDER = 'video/'
SAVED_FOLDER = 'saved/'


def create_image(image_file, image_calculator=None, frame_number=100, video_file="", factorx=10, factory=10, output=None):
    if image_calculator is None and video_file == "":
        raise ValueError("expectted an image calculator or a video file")

    image_calculator = CalculateImageOutOfVideo(video_file, frame_number, well_divided=True) if (
                image_calculator is None) else image_calculator
    image = imageio.imread(image_file, pilmode='RGB')
    image_calculator.calculate_image(image, CompareAverage(), factorx, factory)
    image_calculator.save_image(SAVED_FOLDER + 'saved_' + (output if output is not None else image_file))
    return image_calculator

if __name__ == "__main__":
    create_image(
        image_file="image/sheldon.jpeg", 
        video_file="video/pickle_rick.mp4", 
        frame_number=5)