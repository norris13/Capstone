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

'''
load_data(cols_to_use) is a function which will read in the data and return numpy arrays of the specified fields, split into training and testing datasets

cols_to_use: array of columns to be included in the training and testing datasets. Entries in cols_to_use should be integers

returns two numpy arrays, train and test, which are the training and testing datasets
'''
def load_data(cols_to_use, n_rows):
	train_data = np.genfromtxt('../data/asciipdb2021trv3_us_tabs.txt', delimiter='\t', skip_header=1, 
		encoding=None, dtype=np.float, usecols=cols_to_use, max_rows=n_rows)
	test_data = np.genfromtxt('../data/asciipdb2021trv3_us_tabs.txt', delimiter = '\t', skip_header = 55001, encoding=None, dtype=np.float, usecols = cols_to_use)
	# some of the entries in the array are strings, like monetary values such as "$100,000" so numpy will not read them in as doubles. We need to convert
	# them from strings to integers and then append them back onto the other numpy arrays
	'''
	train_strings = np.genfromtxt('../data/asciipdb2021trv3_us_tabs.txt', delimiter='\t', skip_header=1,
		encoding=None, dtype=str, usecols=stringCols, max_rows=n_rows)
	test_strings = np.genfromtxt('../data/asciipdb2021trv3_us_tabs.txt', delimiter = '\t', skip_header = 55001, encoding=None, dtype=str, usecols = stringCols)

	for i,row in enumerate(test_strings):
		for j,s in enumerate(row):
			test_strings[i,j] = s.replace('$','').replace(',','').replace(' ','').replace('\"','')
	test_strings[test_strings == ''] = 'nan'
	converted = test_strings.astype(np.float)

	for i,row in enumerate(train_strings):
		for j,s in enumerate(row):
			try:
				train_strings[i,j] = s.replace('$','').replace(',','').replace(' ','').replace('\"','')
			except:
				print(row)
				print(s)
				return 3, 4
	train_strings[train_strings == ''] = 'nan'
	converted = train_strings.astype(np.float)

	test = np.concatenate((test_data, test_strings), axis = 1)
	train = np.concatenate((train_data, train_strings), axis = 1)
	test = test.astype(np.float)
	train = train.astype(np.float)
	return train, test
	'''
	return train_data, test_data # delete this
'''
print(test_data.shape)
print(test_data[1])
print(type(test_data[1]))
print(test_data[1][1])
print(test_data[1, 1])
'''
