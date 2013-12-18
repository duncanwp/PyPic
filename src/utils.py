'''
Created on 7 Feb 2013

@author: duncan
'''

#!/usr/bin/python3

#from gi.repository import GExiv2
#
#exif = GExiv2.Metadata('IMG_1234.JPG')
#
## longitude, latitude, altitude
#exif.set_gps_info(-79.3969702721, 43.6295057244, 76)
#
## Using dict notation like this reads/writes RAW string values
## into the EXIF data, with no modification/interpolation by GExiv2.
## Refer to GExiv2.py to see what kind of convenience methods are
## supplied for setting/getting non-string values.
#IPTC = 'Iptc.Application2.'
#exif[IPTC + 'City'] = 'Toronto'
#exif[IPTC + 'ProvinceState'] = 'Ontario'
#exif[IPTC + 'CountryName'] = 'Canada'
#
#exif.save_file()

def print_meta_data(file):
    from exifread import process_file
    
    metadata = process_file(file)
    tag = 'Exif.Image.Model'

    if tag in metadata:
        print('Your camera is a:', metadata[tag])
    else:
        print('Your camera is unknown.')
        
    print 'Keywords: ',metadata.get('Iptc.Application2.Keywords','None')
    print 'Keywords: ',metadata.get('Iptc.Application2.Keywords','None')
    for tag in metadata:
        print tag
#        print metadata['Xmp.dc.subject']
    
#    print('This photo has %d tags.' % len(metadata))
    

# def add_keyword_to_picture(keyword, pic):
#     from gi.repository import GExiv2
#
#     metadata = GExiv2.Metadata(pic)
#
#     if metadata.get('Iptc.Application2.Keywords',None) == keyword:
#         print('Keyword already set to %s.' % keyword)
#     else:
#         print 'Adding Keyword: ', keyword, 'to file: ', pic
#         metadata['Iptc.Application2.Keywords'] = keyword
#
#         if metadata['Iptc.Application2.Keywords'] == keyword:
#             print('Keyword set to %s.' % keyword)
#         else:
#             print('There was a problem setting the IPTC Keywords tag.')
#
#         metadata.save_file()

def find_all_pictures(root):
    import os
    all_filenames = []
    
    for dirname, dirnames, filenames in os.walk(root):
        # print path to all subdirectories first.
#        for subdirname in dirnames:
#            print os.path.join(dirname, subdirname)

        # print path to all filenames.
        for filename in filenames:
            name = os.path.basename(filename).split('.')
            if len(name) > 1 and name[1].lower() in ['jpg', 'jpeg']:
                all_filenames.append(os.path.join(dirname, filename))    
        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
#        if '.git' in dirnames:
#            # don't go into any .git directories.
#            dirnames.remove('.git')

    return all_filenames


def find_full_path_to_picture(pic):
    import os
    root = '/mnt/Media/Pictures'
    
    for dirname, dirnames, filenames in os.walk(root):
        # print path to all subdirectories first.
#        for subdirname in dirnames:
#            print os.path.join(dirname, subdirname)

        # print path to all filenames.
        for filename in filenames:
            name = os.path.basename(filename).split('.')
            if name[0] == pic and name[1] != 'mp4':
                full_path = os.path.join(dirname, filename)
                print 'Found full path: ', full_path
                return full_path
    
        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
#        if '.git' in dirnames:
#            # don't go into any .git directories.
#            dirnames.remove('.git')
    print 'No match found for: ', pic
    return None

# def tag_files_from_aperture():
#     text_file_name = '/home/duncan/Downloads/Olivias first year.txt'
#     text_file = open(text_file_name)
#     text = text_file.read()
#     data = text.decode('utf-16')
#
#     files = []
#     for line in data.split('\n'):
#         tabs = line.split('\t')
#         if len(tabs) > 5:
#             filename = line.split('\t')[0]
#             keywords = line.split('\t')[5]
#             files.append(find_full_path_to_picture(filename))
#
#     for a_file in files:
#         if a_file is not None:
#             add_keyword_to_picture('Olivias photobook', a_file)

# def add_keyword_based_on_rating(files):
#     from gi.repository import GExiv2
#
#     for a_file in files:
#         metadata = GExiv2.Metadata(a_file)
#         rating = metadata.get_rating()
#         if rating == 4:
#             add_keyword_to_picture('4 Star', a_file)
#         elif rating == 5:
#             add_keyword_to_picture('5 Star', a_file)


def move_photo(root, photo, verbose=False):
    import shutil
    import os
    dest = photo.get_dest(root)
    if not os.path.isfile(dest):
        create_new_photo_directory(root, photo.date)
        if verbose: print "Moving " + photo.path + " to " + dest
        shutil.move(photo.path, dest)
    else:
        if verbose: print photo.path + " already exists at " + dest


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


def create_new_photo_directory(base_path, date):
    """
        Given a datetime like object create a new folder so that:
        base_path/year/month/day/ exists as a path
    """
    import os
    import errno
    new_dir = os.path.join(base_path, str(date.year), str(date.month), str(date.day))

    # Try making the leaf directory (and all intermediate ones). Catch the case
    #  where it already exists and ignore it, re-raise anything else
    try:
        os.makedirs(new_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise