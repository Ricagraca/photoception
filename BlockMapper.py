from CompareAlgorithm import CompareAlgorithm


"""
    This mapper, maps blocks from a compressed image
    to an image x with check_image method   
"""

class BlockMapper:

    def __init__(self, compressed_image, compare_algorithm: CompareAlgorithm):
        self.map = dict()
        self.compressed_image = compressed_image
        self.compare_algorithm = compare_algorithm

    """
        Given an image x,
        map the position of the blocks from compressed_image 
        to that image if the difference is lower than the current
    """

    def check_image(self, x):

        magnitude = lambda x, y: (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2
        calculate_image = self.compare_algorithm.calculate(x)

        minimum_length = None
        pos = None
        for j, line in enumerate(self.compressed_image):
            for i, element in enumerate(line):
                length = magnitude(element, calculate_image)
                pos = j, i
                if pos not in self.map or self.map[pos][1] > length:
                    self.map[pos] = x, length
