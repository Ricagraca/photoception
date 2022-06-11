
from CompressImage import CompressImage
from BlockMapper import BlockMapper


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

        vidcap = cv2.VideoCapture(video_path)
        counter = 0
        selected_frames = []

        while success and counter//skip < self.number:
            success, img = vidcap.read()
            if counter % self.skip == 0:
                selected_frames.append(img)
            counter += 1

        self.selected_frames = selected_frames


    def calculate_image(self, image, compare_algorithm, factorx, factory):

        # Check if there are frames first
        if self.selected_frames < 0:
            self.get_frames()

        compressed_image = CompressImage(image, compare_algorithm, factorx, factory)
        block_map = BlockMapper(compressed_image, compare_algorithm)
        
        for frame in self.selected_frames:
            block_map.check_image(frame)

        height, width = len(image), len(image[0])
        height_square = height//factory
        width_square = width//factorx
            
        for pos in block_map.map:
            img, length = block_map.map[pos]
            compressed_image = CompressImage(img, compare_algorithm, width_square, height_square)
            reduced_image = compressed_image.calculate()
            for f in range(factorx):
                print(pos)
                xi = pos[0] * factorx + f
                y1 = pos[1] * factorx
                y2 = y1 + len(reduced_image[f])
                image_ok[xi][y1:y2] = reduced_image[f]

        self.calculated_image = image_ok


    def save_image(self, file_name):
        assert self.calculate_image != None
        cv2.imwrite(file_name, self.calculate_image)  # save frame as JPEG file