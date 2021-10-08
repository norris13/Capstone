import numpy as np
import csv
import sys
import os
path = '../../../.local/lib/python2.7/site-packages/'
from importlib.machinery import SourceFileLoader
d = os.listdir(path) # returns list
sys.path.append(path)
from unidecode import unidecode



def toascii():
    with open(r'../data/pdb2021trv3_us.csv', 'r', encoding='utf8') as origfile, open(r'../data/asciipdb2021trv3_us.csv', 'w', encoding='ascii') as convertfile:
        for line in origfile:
            line = unidecode(line)
            convertfile.write(line)
toascii()
print("done!")
