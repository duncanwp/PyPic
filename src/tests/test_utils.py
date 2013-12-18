from datetime import date

from nose.tools import assert_equal, assert_true
from nose.tools.nontrivial import raises

from src.dates import InvalidDateException

__author__ = 'duncan'
from unittest import TestCase

class test_utils(TestCase):
    photo_dates = {"./test_images/DSC05759.JPG": date(2012, 7, 8),
                   "./test_images/IMG_20121209_104706.jpg": date(2012, 12, 9),
                   "./test_images/DSC01008.jpg": date(2008, 7, 19),
                   "./test_images/DSC01039.jpg": date(2008, 7, 19),
                   "./test_images/2013-10-04 01-04-17-660.jpg": date(2013, 10, 4),
                   "./test_images/DSC06423.JPG": date(2012, 12, 28),
                   "./test_images/2013-07-07 10-36-03-396.jpg": date(2013, 7, 7)}

    valid_exif_file = "./test_images/DSC01039.JPG"
    valid_filename_file = "./test_images/IMG_20121209_104706.jpg"

    def test_exif_parse(self):
        from src.utils import print_image_tags
        #with open(test_utils.valid_exif_file, "rb") as f:
        #    print_image_tags(f)
        print_image_tags(test_utils.valid_exif_file)
