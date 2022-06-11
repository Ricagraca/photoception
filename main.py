
from email.mime import image
import imageio
import scipy as scipy

from CalculateImageOutOfVideo import CalculateImageOutOfVideo
from CompareAverage import CompareAverage

IMAGE_FOLDER = 'image/'
VIDEO_FOLDER = 'video/'


if __name__ == '__main__':

    image_file = 'cn.jpg'

    image_calculator = CalculateImageOutOfVideo(VIDEO_FOLDER + "video.mp4",1000,1000)
    image = imageio.imread(IMAGE_FOLDER + image_file, pilmode='RGB')
    image_calculator.calculate_image(image,CompareAverage(),5,10)
    image_calculator.save_image('saved' + image_file)
