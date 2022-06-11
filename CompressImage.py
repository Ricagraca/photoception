import math

from CompareAlgorithm import CompareAlgorithm

"""
    Given an image, calculate a new compressed image
    factored by factorx, factory and a comparare
    algorithm
"""

class CompressImage:

    def __init__(self, image, compare_algorithm: CompareAlgorithm, factorx, factory):
        self.width = len(image[0])
        self.height = len(image)
        self.image = image
        self.factorx = factorx
        self.factory = factory

        # For now, assert that the factor must divide the width/height
        # print(self.width, self.height, factorx, factory)
        assert (self.width % factorx) == (self.height % self.factory) == 0

        self.compare_algorithm = compare_algorithm

    """
        Calculate the compressed image
    """
    def calculate(self):
        width_resized = self.width // self.factorx
        height_resized = self.height // self.factory

        values = []
        for h in range(height_resized):
            l = []
            for w in range(width_resized):
                h_lines = self.image[h * self.factory:self.factory * (h + 1)]
                factored_image = [line[self.factorx * (w):self.factorx * (w + 1)] for line in h_lines]
                r, g, b = self.compare_algorithm.calculate(factored_image)
                l += [[r, g, b]]

            values += [l]

        return values
