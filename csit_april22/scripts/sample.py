#!/usr/bin/env python
import sys
import os

if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

# print fileDir
Par_Dir = os.path.dirname(fileDir)
# print Par_Dir
sys.path.append(Par_Dir)

from csit.libraries.VersaLib import VersaLib



# cpe = VersaLib('CPE11', topofile="sunitha.yml")
cpe = VersaLib('CPE11', topofile="Devices.yml")