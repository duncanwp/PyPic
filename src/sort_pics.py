#!/usr/bin/python2.7
import argparse

__author__ = 'duncan'

# root = '/home/duncan/Desktop'
# root = '/mnt/Media/Pictures'

parser = argparse.ArgumentParser(description="Sort photos")
parser.add_argument('--dry-run', '-n', help="Dry-run: Simulate results, print output", action='store_true')
parser.add_argument('--validate', '-d', help="Validate: Check that files are in the right folders already", action='store_true')
parser.add_argument('-r', help="Recursively find files below the given folder")
parser.add_argument('-v', help="Verbose", action='store_true')
parser.add_argument('target', metavar='target', help="The file or folder of files to process", nargs='+')


def main():
    from src.photo import Photo
    from src.utils import find_all_pictures, move_photo
    import os

    args = parser.parse_args()
    file_targets = []
    photos = []
    for t in args.target:
        if os.path.isdir(t):
            file_targets.extend(find_all_pictures(t))
        elif os.path.isfile(t):
            file_targets.append(t)

    for f in file_targets:
        photos.append(Photo(f))

    if args.validate:
        for p in photos:
            if not p.valid_path():
                print "Invalid path: " + p.path
    if args.dry_run:
        print "Dry-run:"
        for p in photos:
            print p.path + ": " + str(p.date)
    else:
        print "Sorting files..."
        for p in photos:
            move_photo(root, p, args.v)

if __name__ == "__main__":
    main()
