"""
# Data file specification:

## Fundamentals:
* Data files shall be given the extension .df
* Data files be encoded in valid UTF-8

## Revision ID:
* The first line of a data file shall contain the file's revision ID.
* The revision ID may be any positive number that has the following properties:
    1. A revision ID must be unique for each revision.
    2. The number representing the revision ID must get bigger as time
       progresses.
* An example of a number that fulfills the given requirements is the
  number of seconds since 1. January 1970 (epoch time).

## Data columns:
TODO: Expand further...

Data file example:
```
1543597775.6957102
TODO: Expand further...
```
"""
from time import time

def new_revision_id():
    epoch_time = time()
    return float(epoch_time)

class FileData:
    def __init__(self, file_name):
        self.__file_name = file_name

        try:
            self.read()
        except FileNotFoundError:
            # File did not exist; let's fix that
            self.__revision_id = new_revision_id()
            self.__cache = []
            self.write()

    """
    Reads the data file located at self.__file_name, and sets the following attributes:
        self.__revision_id
        self.__cache

    Does nothing if cache data is newer than file data.
    """
    def read(self):
        with open(self.__file_name, 'r', encoding='utf-8') as df:
            lines = df.readlines()

            df_revision_id = float(lines[0])
            if self.__revision_id < df_revision_id:
                # The data that's in the file is newer than what we've got
                # in our cache.
                # Let's write to file what's in our cache...
                self.__revision_id = df_revision_id

    """
    If cache data is newer than file data, or if no file exists at self.__file_name,
    write the cache data to the file located at self.__file_name.
    """
    def write(self):
        with open(self.__file_name, 'wr+', encoding='utf-8') as df:
            lines = df.readlines()
            if not lines:
                df_revision_id = -1
            else:
                df_revision_id = float(lines[0])

            if self.__revision_id > df_revision_id:
                # The data that's in our cache is newer than what is in the
                # datafile.
                # Write to file what's in our cache...
                pass
