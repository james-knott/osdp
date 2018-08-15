"""
Open Source Development Platform.

"""

import logging
import sys
from ruamel.yaml import YAML
import argparse

__author__ = "James Knott (@Ghettolabs)"
__copyright__ = "Copyright 2018 James Knott"
__credits__ = ["James Knott"]
__license__ = "Apache License, 2.0"
__version__ = "0.0.3"
__maintainer__ = "James Knott"
__email__ = "devops@ghettolabs.io"
__status__ = "Development"



def setup_logging():
    logger = logging.getLogger()
    for h in logger.handlers:
      logger.removeHandler(h)
    h = logging.StreamHandler(sys.stdout)
    FORMAT = "[%(levelname)s %(asctime)s %(filename)s:%(lineno)s - %(funcName)21s() ] %(message)s"
    h.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)
    return logger

if __name__ == "__main__":
    logger = setup_logging()
    logger.info("Welcome to Open Source Development Platform!")
    parser = argparse.ArgumentParser(description='Open Source Development Platform')
    parser.add_argument("--init","-i", required=False, dest='init',action='store_true',help='Initialize new project folder')
    parser.add_argument("--new","-n", required=False, dest='new',action='store_true',help='Create new project from template file')
    parser.add_argument("--update","-u", required=False, dest='update',action='store_true',help='Update settings')
    parser.add_argument("--backup","-b", required=False,dest='backup',action='store_true',help='Sync project to backup device')
    parser.add_argument("--destroy","-e", required=False,dest='destroy',action='store',help='Delete project from folder')
    parser.add_argument("--start","-s", required=False,dest='start',action='store',help='Start services')
    parser.add_argument("--stop","-d", required=False,dest='stop',action='store',help='Stop services')

    result = parser.parse_args()
