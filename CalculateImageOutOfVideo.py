
from CompressImage import CompressImage
from BlockMapper import BlockMapper
import cv2
import numpy as np


class CalculateImageOutOfVideo:

    """
        Function that tells how similar two images are
        The bigger the value, the bigger the difference
    """
    def __init__(self, video_path, number, skip):
        self.video_path = video_path
        self.number = number
        self.skip = skip

    """
        From video, return a number of frames while
        skipping a interval of frames
    """

    def get_frames(self):

        vidcap = cv2.VideoCapture(self.video_path)
        counter = 0
        selected_frames = []
        success = True

        while success and counter//self.skip < self.number:
            success, img = vidcap.read()
            if counter % self.skip == 0:
                selected_frames.append(img)
            counter += 1

        self.selected_frames = selected_frames


    def calculate_image(self, image, compare_algorithm, factorx, factory):

        # Check if there are frames first
        if not hasattr(self, 'selected_frames') or len(self.selected_frames) < 0:
            self.get_frames()


        compressed_image = CompressImage(image, compare_algorithm, factory, factorx).calculate()
        block_map = BlockMapper(compressed_image, compare_algorithm)
        
        # Calculate map for image
        print('Calculating Map')
        for frame in self.selected_frames:
            block_map.check_image(frame)
            
        height = len(image)
        width = len(image[0])

        # Create result image
        image = np.ndarray(shape=(height,width,3))

        # Create Image out of mapping
        print('Creating image out of map')
        for pos in block_map.map:
            img, length = block_map.map[pos]
            compressed_image = CompressImage(img, compare_algorithm, factorx, factory)
            reduced_image = compressed_image.calculate()
            for f in range(factorx):
                x = pos[0] * factorx + f
                y1 = pos[1] * factory
                y2 = y1 + len(reduced_image[f])
                print(x,y1,y2, factorx, factory)
                image[x][y1:y2] = reduced_image[f]

        self.calculated_image = image


    def save_image(self, file_name):
        assert self.calculate_image != None
        cv2.imwrite(file_name, self.calculate_image)  # save frame as JPEG file