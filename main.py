
import cv2
import imageio
import scipy as scipy

from CompareAverage import CompareAverage
from Mapper import Mapper
from ScanImage import ScanImage

if __name__ == '__main__':
    vidcap = cv2.VideoCapture('D:\\Youtube\\v1.mp4')
    success,image_ok = vidcap.read()
    height, width = len(image_ok), len(image_ok[0])
    factor = 10 # math.gcd(height, width)
    print(height, width)
    print(factor)

    im = imageio.imread('D:rickastley.jpg', pilmode='RGB')
    image_ok = im

    ca = CompareAverage()

    # Picture here
    si = ScanImage(image_ok, CompareAverage(), factor, factor)
    print(len(image_ok), len(image_ok[0])) # 360 640
    reduced_image = si.calculate()
    print(len(reduced_image), len(reduced_image[0])) # 36 64
    m = Mapper(reduced_image, ca)

    counter = 0
    limit = 1000000000
    skip = 100
    while success and counter < limit:
        success, img = vidcap.read()
        if counter % skip == 0:
            m.check_image(img)
        counter += 1

    # Create image
    print('creating image')
    height_square = height//factor
    width_square = width//factor
    for pos in m.map:
        img, length = m.map[pos]
        si = ScanImage(img, CompareAverage(), 64, 36)
        reduced_image = si.calculate()
        print(len(reduced_image), len(reduced_image[0])) # 36 64
        # write image
        # Need to write line by line
        #
        for f in range(factor):
            print(pos)
            xi = pos[0] * factor + f
            y1 = pos[1] * factor
            y2 = y1 + len(reduced_image[f])
            print(xi, y1, y2)
            image_ok[xi][y1:y2] = reduced_image[f]

    cv2.imwrite("frame.jpg", image_ok)  # save frame as JPEG file

