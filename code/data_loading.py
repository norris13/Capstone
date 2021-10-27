import numpy as np
import csv
import sys
import os
path = '../../../.local/lib/python2.7/site-packages/'
from importlib.machinery import SourceFileLoader
sys.path.append(path)
import unidecode



'''
get_columns()
	getColumns reads in the first row (column headers) from the csv file and then returns the column indeces
	of the csv file we wish to use. Specifically, it will return all of the columns which are not strings and
	are not margin of error columns. We do not care about the margin of errors when *training* the model. We
	are ignoring the strings *in this method* because you cannot read the csv into numpy if it contains multiple 
	different types (floats and strings, for instance). Values like "$251,432", while they can be converted to
	float, are not yet floats. This conversion will be done in the load_data() function.

returns:
	a list of column indeces to be used by load_data()

'''
def get_columns_for_reading():

	# open the file, read in the first row which are the column names. append those values to colnames
	colnames = []
	with open('../data/asciipdb2021trv3_us.csv', newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			colnames = row
			break

	# note that columns 2 and 4 are also strings, but they are state and county names and are 
	# represented elsewhere as numerical values. The model doesn't need both.
	# The following columns need to be read in as strings
	stringCols = [0, 1, 3, 5, 254, 219, 220, 221, 222, 255, 256, 257,  469, 470, 499, 500] 
	
	# the column indeces of the csv we want to read in. All values which are not strings or MOE
	cols_to_use = []
	names = []
	for (i, col) in enumerate(colnames):
		if "MOE" not in col and i not in stringCols and i not in [2, 4]:
			cols_to_use.append(i)
			names.append(col)

	return cols_to_use, names

'''
load_data(cols_to_use, n_rows = 55000, include_strings = True) 
		A function which will read in the data and return numpy arrays of the specified fields, split into training and testing datasets

cols_to_use: array of columns to be included in the training and testing datasets. Entries in cols_to_use should be integers
n_rows: number of rows to read in to the training dataset
include_strings: do you want the string columns

returns two numpy arrays, train and test, which are the training and testing datasets
'''
def load_data(cols_to_use, n_rows = 55000, include_strings = False):
	
	# read in the float values from the csv
	train_data = np.genfromtxt('../data/asciipdb2021trv3_us_tabs.txt', delimiter='\t', skip_header=1, 
		encoding=None, dtype=np.float, usecols=cols_to_use, max_rows=n_rows)
	test_data = np.genfromtxt('../data/asciipdb2021trv3_us_tabs.txt', delimiter = '\t', skip_header = 55001, encoding=None, dtype=np.float, usecols = cols_to_use)
	# some of the entries in the array are strings, like monetary values such as "$100,000" so numpy will not read them in as doubles. We need to convert
	# them from strings to integers and then append them back onto the other numpy arrays
	
	stringCols = [0, 1, 3, 5, 254, 219, 220, 221, 222, 255, 256, 257,  469, 470, 499, 500] # The following columns need to be read in as strings
	
	# read in the strings
	if include_strings == False:
		return train_data, test_data
	else:
		train_strings = np.genfromtxt('../data/asciipdb2021trv3_us_tabs.txt', delimiter='\t', skip_header=1,
			encoding=None, dtype=str, usecols=stringCols, max_rows=n_rows)
		test_strings = np.genfromtxt('../data/asciipdb2021trv3_us_tabs.txt', delimiter = '\t', skip_header = 55001, encoding=None, dtype=str, usecols = stringCols)

		# for each index(i) and actual row (row) in test_strings
		for i,row in enumerate(test_strings):
			# for each column index (j) and actual string entry (s) in row
			for j,s in enumerate(row):
				# try to replace all non 0-9 characters with nothing
				try:
					test_strings[i,j] = s.replace('$','').replace(',','').replace(' ','').replace('\"','')
				except:
					pass
		
		# all empty values will be replaced with nan (not a number)
		test_strings[test_strings == ''] = 'nan'
		# convert the strings to floats
		converted = test_strings.astype(np.float)

		# repeat above process but for train_strings
		for i,row in enumerate(train_strings):
			for j,s in enumerate(row):
				try:
					train_strings[i,j] = s.replace('$','').replace(',','').replace(' ','').replace('\"','')
				except:
					pass
		train_strings[train_strings == ''] = 'nan'
		converted = train_strings.astype(np.float)

		# append the columns which WERE strings to their respective numpy float matrix
		test = np.concatenate((test_data, test_strings), axis = 1)
		train = np.concatenate((train_data, train_strings), axis = 1)

		# recast the whole matrix as a float
		test = test.astype(np.float)
		train = train.astype(np.float)

		# return the final train and test datasets
		return train, test
	
