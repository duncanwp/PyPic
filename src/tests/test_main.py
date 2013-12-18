from datetime import date

from dates import InvalidDateException


__author__ = 'duncan'
from unittest import TestCase

class test_dates(TestCase):
    photo_dates = {"./test_images/DSC05759.JPG": date(2012, 7, 8),
                   "./test_images/IMG_20121209_104706.jpg": date(2012, 12, 9),
                   "./test_images/DSC01008.jpg": date(2008, 7, 19),
                   "./test_images/DSC01039.jpg": date(2008, 7, 19),
                   "./test_images/2013-10-04 01-04-17-660.jpg": date(2013, 10, 4),
                   "./test_images/DSC06423.JPG": date(2012, 12, 28),
                   "./test_images/2013-07-07 10-36-03-396.jpg": date(2013, 7, 7)}

    valid_exif_file = "./test_images/DSC05759.JPG"
    valid_filename_file = "./test_images/IMG_20121209_104706.jpg"

    def test_dont_overwrite(self):
        from src.utils import move_photo
        from src.photo import Photo
        move_photo("./test_images", Photo("./test_images/50758.JPG"))
