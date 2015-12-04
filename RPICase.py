__author__ = 'flo'
import csv
import numpy as np
from NumericToNominalConverter import NumericToNominalConverter

"""Read in the final_table obtained from the feature_extraction script"""
with open("tables/final_table.csv",'r') as dest_f:
    data_iter = csv.reader(dest_f,
                           delimiter = ',')
    header = next(data_iter)
    data_types = next(data_iter)
    data = [data for data in data_iter]
data_array = np.asarray(data, dtype = None)

"""Convert all numeric attributes to nominal (beta)"""
for i in range(len(data_types) - 1):
    if data_types[i] == 'numeric':
        data_array[:,i] = NumericToNominalConverter(data_array[:,i], num_bins=10).convert()

"""
    x : features
    y : classes
    Todo:
    Create training- and test data
    train models (naive bayes, logistic regression, SVM)
    evaluate models
    plot ROC curves for each model
"""
y = data_array[:, 0]
x = data_array[:, 1:]