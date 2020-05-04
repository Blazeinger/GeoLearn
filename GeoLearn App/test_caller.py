import os
import sys
from subprocess import run,PIPE

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
TARGET_DIR = CURR_DIR.replace( "/", "//" )  + "//python_scripts" 

print( TARGET_DIR + "//test.py" )

run([sys.executable, TARGET_DIR + '//test.py'],  shell=False, stdout=PIPE)
