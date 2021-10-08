import numpy as np
import csv
import sys
import os
path = '../../../.local/lib/python2.7/site-packages/'
from importlib.machinery import SourceFileLoader
d = os.listdir(path) # returns list
sys.path.append(path)
import unidecode
colnames = []
with open('../data/asciipdb2021trv3_us.csv', newline='') as f:
	reader = csv.reader(f)
	for row in reader:
		colnames = row
		break


stringCols = [0, 1, 3, 5, 254, 219, 220, 221, 222, 255, 256, 257,  469, 470, 499, 500] # The following columns need to be read in as strings
# note that columns 2 and 4 are also strings, but they are state and county names and are represented elsewhere as numerical values. The model doesn't need both.
cols_to_use = []
for (i, col) in enumerate(colnames):
	if "MOE" not in col and i not in stringCols and i not in [2, 4]:
		cols_to_use.append(i)


def load_data(cols_to_use):
	train_data = np.genfromtxt('../data/asciipdb2021trv3_us_tabs.txt', delimiter='\t', skip_header=1, encoding=None, dtype='f', usecols=cols_to_use, max_rows=55000)
	test_data = np.genfromtxt('../data/asciipdb2021trv3_us_tabs.txt', delimiter = '\t', skip_header = 55001, encoding=None, dtype='f', usecols = cols_to_use)
	# some of the entries in the array are strings, like monetary values such as "$100,000" so numpy will not read them in as doubles. We need to convert
	# them from strings to integers and then append them back onto the other numpy arrays
	train_strings = np.genfromtxt('../data/asciipdb2021trv3_us_tabs.txt', delimiter='\t', skip_header=1,
		encoding=None, dtype='f', usecols=convToString, max_rows=55000)
	test_strings = np.genfromtxt('../data/asciipdb2021trv3_us_tabs.txt', delimiter = '\t', skip_header = 55001, encoding=None, dtype=str, usecols = stringCols)

	for i,row in enumerate(test_strings):
		for j,s in enumerate(row):
			test_strings[i,j] = s.replace('$','').replace(',','').replace(' ','').replace('\"','')
	test_strings[test_strings == ''] = 'nan'
	converted = test_strings.astype(np.float)

	for i,row in enumerate(train_strings):
                for j,s in enumerate(row):
                        train_strings[i,j] = s.replace('$','').replace(',','').replace(' ','').replace('\"','')
        train_strings[train_strings == ''] = 'nan'
        converted = train_strings.astype(np.float)

	test = np.concatenate((test_data, test_strings), axis = 1)
	train = np.concatenate((train_data, train_strings), axis = 1)
	return train, test
'''
print(test_data.shape)
print(test_data[1])
print(type(test_data[1]))
print(test_data[1][1])
print(test_data[1, 1])
'''
load_data()
