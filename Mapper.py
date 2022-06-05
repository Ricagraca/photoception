from CompareAlgorithm import CompareAlgorithm


class Mapper:

    def __init__(self, compressed_image, compare_algorithm: CompareAlgorithm):
        self.map = dict()
        self.compressed_image = compressed_image
        self.compare_algorithm = compare_algorithm

    def check_image(self, image):

        magnitude = lambda x, y: (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2
        calculate_image = self.compare_algorithm.calculate(image)

        minimum_length = None
        pos = None
        for j, line in enumerate(self.compressed_image):
            for i, element in enumerate(line):
                length = magnitude(element, calculate_image)
                pos = j, i
                if pos not in self.map or self.map[pos][1] > length:
                    self.map[pos] = image, length
