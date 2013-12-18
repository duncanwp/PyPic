'''
Created on 7 Feb 2013

@author: duncan
'''


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