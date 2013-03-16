import os

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
ASSETS_PATH = os.path.join(PROJECT_DIR, 'assets')
ACCEL_CSV_FILES = [
  os.path.join(PROJECT_DIR, 'data', 'accel_1.csv'),
  os.path.join(PROJECT_DIR, 'data', 'accel_2.csv'),
]
FSR_CSV_FILE = os.path.join(PROJECT_DIR, 'data', 'fsrout.csv')
NN_FILE = os.path.join(PROJECT_DIR, '..', 'training', 'network-good.pickle')

ACCEL_UPDATE = 250
FSR_UPDATE = 250
EMPTY_THRESHOLD=300
