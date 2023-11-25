import sys
import os

os.chdir("/home/user123/search")
sys.path.append("/home/user123/search")

from app import app

application = app
