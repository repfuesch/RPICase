__author__ = 'flo'
import csv
import numpy as np
from NumericToNominalConverter import NumericToNominalConverter

with open("tables/final_table.csv",'r') as dest_f:
    data_iter = csv.reader(dest_f,
                           delimiter = ',')
    header = next(data_iter)
    data_types = next(data_iter)
    data = [data for data in data_iter]
data_array = np.asarray(data, dtype = None)

for type in data_types:
    if type == 'numeric':
        for idx in range(0, len(data_types) - 1):
            if data_types[idx] == 'numeric':
                print(data_array[:,idx])
                data_array[:,idx] = NumericToNominalConverter(data_array[:,idx], num_bins=10).convert()

for row in data_array:
    print(row)