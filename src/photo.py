from src.dates import get_photo_date

__author__ = 'duncan'


class Photo:

    def __init__(self, org_path, date=None):
        import os
        self.path = org_path
        self.dir = os.path.dirname(org_path)
        self.filename = os.path.basename(org_path)
        self.extension = os.path.splitext(self.filename)[1]
        if date is None:
            try:
                self.date = get_photo_date(self.path)
            except:
                self.date = "NO DATE"
        else:
            self.date = date

    def get_dest(self, root):
        import os.path as p
        return p.join(root, str(self.date.year).zfill(2), str(self.date.month).zfill(2), str(self.date.day).zfill(2),
                      self.filename)

    def valid_path(self):
        path_elements = self.dir.split('/')
        year = path_elements[-3]
        month = path_elements[-2]
        day = path_elements[-1]
        return int(year) == self.date.year and int(month) == self.date.month and int(day) == self.date.day