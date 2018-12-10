import os
import sys
from appdirs import user_data_dir, user_log_dir

# Information for humans:
# -----------------------------------------------------------------------------
APPNAME = 'Auto-Rental'
AUTHOR = 'hopur-32'

# Information for computers:
# -----------------------------------------------------------------------------
DATA_DIR = user_data_dir(APPNAME, AUTHOR) # OS specific directory to store data
if not os.path.isdir(DATA_DIR):
    os.makedirs(DATA_DIR)

if sys.platform == 'linux':
    LOGGING_DIR = '/tmp'
else:
    LOGGING_DIR = user_log_dir(APPNAME, AUTHOR)
    if not os.path.isdir(LOGGING_DIR):
        os.makedirs(LOGGING_DIR)
