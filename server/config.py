import os
import configparser
from .constants import ROOT_DIR

CONFIG = configparser.ConfigParser()
CONFIG.read(
    os.path.join(ROOT_DIR, 'server.ini')
)
