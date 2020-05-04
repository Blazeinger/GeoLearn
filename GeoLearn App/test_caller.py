import os
import sys
from subprocess import run,PIPE

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
TARGET_DIR = CURR_DIR.replace( "/", "//" )  + "//python_scripts//biodiversity" 

target = TARGET_DIR + "//biodiversity_image_scraper.py" 
print( target )

run([sys.executable, target],  shell=False, stdout=PIPE)
