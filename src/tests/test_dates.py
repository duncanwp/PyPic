from datetime import date

from nose.tools import assert_equal, assert_true
from nose.tools.nontrivial import raises

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

    def test_get_dates_all(self):
        from src.dates import get_photo_date
        for p, d in test_dates.photo_dates.iteritems():
            assert_equal(get_photo_date(p), d)

    def test_valid_path(self):
        from src.photo import Photo
        p = Photo("./test_images/2012/07/08/DSC05759.JPG")
        assert_true(p.valid_path())

    def test_get_dates_by_exif_tag_returns_created_date_Samsung_Galaxy_Nexus(self):
        from src.dates import get_date_from_exif_tag
        valid_date = date(2012,7,8)
        assert_equal(get_date_from_exif_tag(test_dates.valid_exif_file), valid_date)

    def test_get_dates_by_exif_tag_returns_created_date_Sony_cam(self):
        from src.dates import get_date_from_exif_tag
        valid_date = date(2012,12,9)
        assert_equal(get_date_from_exif_tag(test_dates.valid_filename_file), valid_date)

    def test_get_dates_by_filename_returns_created_date(self):
        from src.dates import get_date_from_filename
        valid_date = date(2012,12,9)
        assert_equal(get_date_from_filename(test_dates.valid_filename_file), valid_date)

    @raises(InvalidDateException)
    def test_get_dates_by_filename_returns_created_date_fails_for_invalid_filename(self):
        from src.dates import get_date_from_filename
        valid_date = date(2012,12,9)
        assert_equal(get_date_from_filename(test_dates.valid_exif_file), valid_date)
