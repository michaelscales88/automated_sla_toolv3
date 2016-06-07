import datetime
import os
import sys

from os import path
from src.email_reader import (get_downloads)

os.path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

now = datetime.datetime.today()
get_downloads(now, 'Archive')
get_downloads(now, 'raw')
