from email.mime import image
import imageio
import scipy as scipy
import os.path
import cv2
from os import path

from src.CalculateImageOutOfVideo import CalculateImageOutOfVideo, number_of_frames, video_porportion
from src.CompareAverage import CompareAverage

IMAGE_FOLDER = 'image/'
VIDEO_FOLDER = 'video/'
SAVED_FOLDER = 'saved/'


def create_image(image_file, image_calculator=None, frame_number=100, video_file="", factorx=10, factory=10, output=None):
    if image_calculator is None and video_file == "":
        raise ValueError("expected an image calculator or a video file")

    # Read image
    image = imageio.imread(image_file, pilmode='RGB')

    # Create image calculator instance
    image_calculator = CalculateImageOutOfVideo(video_file, frame_number, well_divided=True) if (
                image_calculator is None) else image_calculator
   
    # Convert image to image with frames out of the video
    image_calculator.calculate_image(image, CompareAverage(), factorx, factory)

    # Save created image
    image_calculator.save_image(SAVED_FOLDER + 'saved_' + (output if output is not None else image_file))
    return image_calculator

if __name__ == "__main__":
    create_image(
        image_file="image/dwight.jpg", 
        video_file="video/pickle_rick.mp4", 
        frame_number=5,
        factorx=10,
        factory=10)