import os
from os import path

from CompressImage import CompressImage
from BlockMapper import BlockMapper
import cv2
import numpy as np
import math
import click

def number_of_frames(video_path):
    vidcap = cv2.VideoCapture(video_path)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    return length


def video_porportion(video_path):
    vidcap = cv2.VideoCapture(video_path)
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    return height, width


class CalculateImageOutOfVideo:
    """
        Function that tells how similar two images are
        The bigger the value, the bigger the difference
    """

    def __init__(self, video_path, number, well_divided=False, skip=1):
        self.video_path = video_path
        self.number = number
        self.height, self.width = None, None
        self.skip = number_of_frames(video_path) // number if well_divided else skip

    """
        From video, return a number of frames while
        skipping a interval of frames
    """

    def get_frames(self):

        vidcap = cv2.VideoCapture(self.video_path)
        counter = 0
        selected_frames = []
        success = True

        print("Getting video frames")
        while success and counter // self.skip < self.number:
            success, img = vidcap.read()
            self.height, self.width = len(img), len(img[0])
            if counter % self.skip == 0:
                selected_frames.append(img)
            counter += 1

        self.selected_frames = selected_frames

    def calculate_image(self, image, compare_algorithm, factorx, factory):

        # Check if there are frames first
        if not hasattr(self, 'selected_frames') or len(self.selected_frames) < 0:
            self.get_frames()

        # Compress image with factory and factorx
        reduced_image = CompressImage(image, compare_algorithm, factory, factorx).calculate()
        block_map = BlockMapper(reduced_image, compare_algorithm)

        # Calculate map for image
        print('Calculating Map')
        for frame in self.selected_frames:
            block_map.check_image(frame)

        return self.create_image_out_of_mapping(image, block_map, compare_algorithm, factory, factorx)

    def create_image_out_of_mapping(self, image, block_map, compare_algorithm, factory, factorx):

        height = len(image)
        width = len(image[0])

        # Create result image
        image = np.ndarray(shape=(height, width, 3))

        # Create Image out of mapping
        print('Creating image out of map')
        print(factorx, factory, len(block_map.map))

        positions = [pos for pos in block_map.map]

        with click.progressbar(range(len(positions))) as bar:
            for pos in bar:
                pos = positions[pos]
                img, length = block_map.map[pos]
                img_height, img_width = len(img), len(img[0])
                block_height, block_width = int(math.ceil(img_height / factory)), int(math.ceil(img_width / factorx))
                reduced_image = CompressImage(img, compare_algorithm, block_width, block_height).calculate()
                for f in range(len(reduced_image)):
                    y = min(pos[0] * factory + f, height - 1)
                    x1 = pos[1] * factorx
                    x2 = min(x1 + len(reduced_image[f]), len(image[y]))
                    # print(y,x1,x2, factorx, factory)
                    image[y][x1:x2] = reduced_image[f][:x2 - x1]

        print("Created image successfully")
        self.calculated_image = image
        return image

    def save_image(self, file_name):
        # assert self.calculated_image != None
        print("Saved image in " + file_name)
        folder = '/'.join(file_name.split('/')[:-1])
        if not path.exists(folder):
            os.mkdir(folder)
        cv2.imwrite(file_name, self.calculated_image)  # save frame as JPEG file
