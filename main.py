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


def create_several(image_file, video_file, frame_number, number_images):
    image_file_name_without_extension = image_file.split(".")[0]
    video_file_name_without_extension = video_file.split(".")[0]

    extension = image_file.split(".")[1]
    saving_directory = SAVED_FOLDER + image_file_name_without_extension + '_' + video_file_name_without_extension + '/'

    height = 256
    width = 256

    image_calculator = CalculateImageOutOfVideo(VIDEO_FOLDER + video_file, frame_number, well_divided=True)
    image = imageio.imread(IMAGE_FOLDER + image_file, pilmode='RGB')

    if not path.exists(saving_directory):
        os.mkdir(saving_directory)

    for i in range(1, number_images + 1):
        saved_file_name = image_file_name_without_extension + str(i) + '.' + extension
        if path.exists(saving_directory + saved_file_name):
            print("File " + saving_directory + saved_file_name + " exists.")
            continue

        factory_, factorx_ = height // (i), width // (i)
        image_calculator.calculate_image(image, CompareAverage(), factorx_, factory_)
        image_calculator.save_image(saving_directory + saved_file_name)


def video_out_of_video(video1, video2, frame_number, number=10, factorx=40, factory=40, file_path="output.mp4",
                       skip=None):
    # Video input
    image_calculator = CalculateImageOutOfVideo(video1, frame_number, well_divided=True)

    # Video for output
    vidcap = cv2.VideoCapture(video2)
    counter = 0
    success = True

    # Create output video writer
    h, w = video_porportion(video1)

    if h is None or w is None:
        raise ValueError("height or width are None")

    fps = 2
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(file_path, fourcc, fps, (w, h))

    skip = (number_of_frames(video_path=video2) // number) if skip is None else skip

    print("Creating video")
    while success and counter // skip < number:
        # Get image from video for output
        success, img = vidcap.read()
        counter += 1
        if counter % skip != 0:
            continue

        print("Creating frame ", counter // skip)
        # Calculate image out of the input video
        calculated_image = image_calculator.calculate_image(img, CompareAverage(), factorx=factorx, factory=factory)

        # Write image to output 
        writer.write(calculated_image)

    writer.release()


# Create image
if __name__ == "__main__":
    create_image(image_file="image/me.jpg", video_file="video/pickle_rick.mp4", frame_number=5, factorx=25, factory=25)

"""
if __name__ == '__main__':
    video_1 = VIDEO_FOLDER + 'pickle_rick.mp4'
    video_2 = VIDEO_FOLDER + 'stay_with_me.mp4'
    frame_number = 2

    video_out_of_video(video_1, video_2, frame_number)
"""