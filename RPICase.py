__author__ = 'flo'

import csv
import numpy as np
from NumericToNominalConverter import NumericToNominalConverter
from sklearn.cross_validation import train_test_split
from PredictionModel import *

#read the final table obtained from the features_extraction.py script
with open("tables/final_table.csv",'r') as dest_f:
    data_iter = csv.reader(dest_f, delimiter = ',')
    header = next(data_iter)
    data_types = next(data_iter)
    data = [data for data in data_iter]
data_array = np.array(data, dtype = float)

if len(data_array) % 2 != 0:
    np.delete(data_array, 1, 0)

#Naive Bayes

#Convert all numeric attributes to nominal (beta)
nominal_array = data_array
for i in range(len(data_types) - 1):
    if data_types[i] == 'numeric':
        nominal_array[:,i] = NumericToNominalConverter(nominal_array[:,i], num_bins=100).convert()

#training and test data for naive bayes
x_train, x_test, y_train, y_test = train_test_split(nominal_array[:, 2:], nominal_array[:, 1], test_size=.5, random_state=0)

bayes = NaiveBayes()
bayes.fit(x_train, y_train)
bayes.predict(x_test, y_test)
print("Accuracy Bayes: " + str(bayes.get_accuracy()))


#training and test data for logistic regression
x_train, x_test, y_train, y_test = train_test_split(data_array[:, 2:], data_array[:, 1], test_size=.5, random_state=0)


#logistic regression
regression = LogisticRegression()
regression.fit(x_train, y_train)
regression.predict(x_test, y_test)
print("Accuracy Logistic Regression: " + str(regression.get_accuracy()))


#print base rate
print("Base rate: " + str(regression.get_base_rate()))

#plot roc curves
fpr, tpr, auc = bayes.get_roc()
plot_roc(fpr, tpr, auc)
fpr, tpr, auc = regression.get_roc()
plot_roc(fpr, tpr, auc)