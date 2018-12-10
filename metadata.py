import os
from appdirs import user_data_dir

# Information for humans:
# -----------------------------------------------------------------------------
APPNAME = 'Auto-Rental'
AUTHOR = 'hopur-32'

# Information for computers:
# -----------------------------------------------------------------------------
DATA_DIR = user_data_dir(APPNAME, AUTHOR) # OS specific directory to store data

if not os.path.isdir(DATA_DIR):
    os.makedirs(DATA_DIR)
