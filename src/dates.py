__author__ = 'duncan'

class NoHeaderException(BaseException):
    pass

class InvalidDateException(BaseException):
    pass

def get_date_from_exif_tag(file):
    from datetime import datetime
    from exifread import process_file

    metadata = process_file(open(file))

    try:
        date_tag = str(metadata['EXIF DateTimeOriginal'])
    except:
        raise NoHeaderException("Exif.Image.DateTime tag not found in: "+file)

    try:
        dt = datetime.strptime(date_tag, "%Y:%m:%d %H:%M:%S")
    except:
        raise InvalidDateException("Invalid date in exif header: "+file)

    return dt.date()


def get_date_from_filename(file):
    """
        Get date from filename, this is quite a general utility which will return a datetime object from a filename type
        string where the filename part is of the form either:
          yyyymmdd*
          or
          ????yyyymmdd*
    """
    from datetime import date
    from os.path import basename
    from src.dates import InvalidDateException

    filename = basename(file)
    try:
        d = date(int(filename[4:8]), int(filename[8:10]), int(filename[10:12]))
    except:
        #
        try:
            d = date(int(filename[0:4]), int(filename[4:6]), int(filename[6:8]))
        except:
            raise InvalidDateException("Couldn't determine date by filename: "+file)
    return d


def get_photo_date(file):
    """
        Try and determine the date of a photo from it's exif header and then by it's filename. Will raise
        an InvalidDateException (out of get_date_from_filename) if it really can't get a date.
    """
    try:
        return get_date_from_exif_tag(file)
    except:
        pass

    return get_date_from_filename(file)
