import math

from CompareAlgorithm import CompareAlgorithm


class ScanImage:

    def __init__(self, image, compare_algorithm: CompareAlgorithm):
        self.width = len(image[0])
        self.height = len(image)
        self.image = image
        self.factor = 10 # math.gcd(self.width, self.height)
        self.compare_algorithm = compare_algorithm

    def calculate(self):
        width_resized = self.factor
        height_resized = self.factor

        values = []
        for h in range(height_resized):
            l = []
            for w in range(width_resized):
                h_lines = self.image[h * self.factor:self.factor * (h + 1)]
                factored_image = [line[self.factor * (w):self.factor * (w + 1)] for line in h_lines]
                r, g, b = self.compare_algorithm.calculate(factored_image)
                l += [[r, g, b]]

            values += [l]

        return values
