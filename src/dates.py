__author__ = 'duncan'

class NoHeaderException(BaseException):
    pass

class InvalidDateException(BaseException):
    pass

def get_date_from_exif_tag(file):
    from datetime import datetime
    from exifread import process_file

    metadata = process_file(file)

    try:
        date_tag = metadata['Exif.Photo.DateTimeOriginal']
    except:
        raise NoHeaderException("Exif.Image.DateTime tag not found in: "+file)

    try:
        dt = datetime.strptime(date_tag, "%Y:%m:%d %H:%M:%S")
    except:
        raise InvalidDateException("Invalid date in exif header: "+file)

    return dt.date()


def get_photo_date(file):
    """
        Try and determine the date of a photo from it's exif header and then by it's filename. Will raise
        an InvalidDateException (out of get_date_from_filename) if it really can't get a date.
    """
    from src.utils import get_date_from_filename
    try:
        return get_date_from_exif_tag(file)
    except:
        pass

    return get_date_from_filename(file)