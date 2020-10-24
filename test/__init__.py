import os
import sys
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(PROJECT_PATH, "src")
sys.path.append(SOURCE_PATH)
TEST_PATH = os.path.join(PROJECT_PATH, "test")
sys.path.append(TEST_PATH)
