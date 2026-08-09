import os
import sys


# Current directory
lib_path = os.path.dirname(os.path.abspath(__file__))

# Add library path
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

# Load fxcorepy
from . import fxcorepy
