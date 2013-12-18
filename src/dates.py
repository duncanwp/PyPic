__author__ = 'duncan'

months = {'01': 'JAN', '02': 'FEB', '03': 'MAR', '04': 'APR', '05': 'MAY',
          '06': 'JUN', '07': 'JUL', '08': 'AUG', '09': 'SEP', '10': 'OCT',
          '11': 'NOV', '12': 'DEC'}

class NoHeaderException(BaseException):
    pass

class InvalidDateException(BaseException):
    pass

def get_date_from_exif_tag(file):
    from datetime import datetime
    from exifread import process_file

    metadata = process_file(open(file))

    if 'EXIF DateTimeOriginal' in metadata:
        date_tag = str(metadata['EXIF DateTimeOriginal'])
    elif'EXIF DateTimeDigitized' in metadata:
        date_tag = str(metadata['EXIF DateTimeDigitized'])
    # elif'Image DateTime' in metadata:
    #     date_tag = str(metadata['Image DateTime'])
    else:
        raise NoHeaderException("No date tags found in: "+file)

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


def parse_date_tstamp(fname):
    """extract date info from file timestamp"""
    import os
    import time
    import datetime

    # Modification of --> Miles (http://stackoverflow.com/questions/946967/get-file-creation-time-with-python-on-mac)
    def get_creation_time(path):
        import sys
        import subprocess
        if sys.platform.startswith('linux'):
            flag = '-c %Y'
        else:  # OS X
            flag = '-f %B'

        p = subprocess.Popen(['stat', flag, path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.wait():
            raise OSError(p.stderr.read().rstrip())
        else:
            return int(p.stdout.read())

    # time of last modification
    if os.name == 'nt':  # windows allows direct access to creation date
        creation_time = os.path.getctime(fname)
    else:
        creation_time = get_creation_time(fname)

    date = datetime.date.fromtimestamp(creation_time)
    # year = str(date.tm_year)
    # month = '{0:02d}'.format(date.tm_mon)
    # month += '-' + months[month]
    # day = '{0:02d}'.format(date.tm_mday)

    return date



def get_photo_date(file, exif=True):
    """
        Try and determine the date of a photo from it's exif header and then by it's filename. Will raise
        an InvalidDateException (out of get_date_from_filename) if it really can't get a date.
    """
    date = None
    if exif:
        try:
            date = get_date_from_exif_tag(file)
        except BaseException as e:
            print e
            date = parse_date_tstamp(file)
    else:
        date = get_date_from_filename(file)

    return date
