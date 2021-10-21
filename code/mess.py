import csv
import numpy as np
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import LinearRegression
from  data_loading import *
from time import time
import pickle

print("Running train_models.py")

colnames = []
with open('../data/asciipdb2021trv3_us.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
                colnames = row
                break


stringCols = [0, 1, 3, 5, 254, 219, 220, 221, 222, 255, 256, 257,  469, 470, 499, 500] # The following columns need to be read in as strings
# note that columns 2 and 4 are also strings, but they are state and county names and are represented elsewhere as numerical values. The model doesn't need both.
cols_to_use = [282]
names = ['dummy']
# cols 288 - 513 contain the percentage variables we are about
for (i, col) in enumerate(colnames):
        if "MOE" not in col and i not in stringCols and i not in [2, 4] and i >= 287 and i < 513:
                if i == 288:
                        print(col)
                cols_to_use.append(i)
                names.append(col)


loaded_model = pickle.load(open('../models/finalized_model.sav', 'rb'))

mask = loaded_model.get_support()
mask = list(mask)
mask.insert(0, False)
print(mask)

for i in (np.array(cols_to_use)[np.array(mask)]):
	print(names[cols_to_use.index(i)])


