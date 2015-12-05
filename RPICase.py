__author__ = 'flo'
import csv
import numpy as np
from NumericToNominalConverter import NumericToNominalConverter
import sklearn.naive_bayes as nb

"""Read in the final_table obtained from the feature_extraction script"""
with open("tables/final_table.csv",'r') as dest_f:
    data_iter = csv.reader(dest_f, delimiter = ',')
    header = next(data_iter)
    data_types = next(data_iter)
    data = [data for data in data_iter]
data_array = np.array(data, dtype = float)

"""Convert all numeric attributes to nominal (beta)"""
for i in range(len(data_types) - 1):
    if data_types[i] == 'numeric':
        data_array[:,i] = NumericToNominalConverter(data_array[:,i], num_bins=10).convert()

"""
    Todo:
    Create training- and test data
    train models (naive bayes, logistic regression, SVM)
    evaluate models
    plot ROC curves for each model
"""

"""Naive Bayes"""
msk = np.random.rand(len(data_array)) < 0.7
training_set = data_array[msk]
test_set = data_array[~msk]
y_train = training_set[:, 1]
x_train = training_set[:, 2:]

y_test = test_set[:, 1]
x_test = test_set[:, 2:]

bayes = nb.MultinomialNB()
bayes.fit(x_train, y_train)

y_pred = bayes.predict(x_test)
pred_wrong = (y_test != y_pred).sum()
print("Accuracy: " + str(float(len(y_test) - pred_wrong) / float(len(y_test))))
pos_samples = (y_test == 1).sum()
neg_samples = len(y_test) - pos_samples

if neg_samples > pos_samples:
    print("Base rate: " + str(float(neg_samples) / float(len(y_test))))
else:
    print("Base rate: " + str(float(pos_samples) / float(len(y_test))))


"""SVM"""

"""Logistic regression"""