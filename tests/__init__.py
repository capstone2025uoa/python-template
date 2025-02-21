# Python is a terribly designed language for testing.
# We need to add the src directory to the path so that we can import the modules.

import os
import sys
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"src"
)
sys.path.append(SOURCE_PATH)