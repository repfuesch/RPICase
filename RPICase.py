__author__ = 'flo'

import csv
import numpy as np
from sklearn.cross_validation import train_test_split
from PredictionModel import *

#read the final table obtained from the features_extraction.py script
def read_csv(filename):
    with open(filename,'r') as dest_f:
        data_iter = csv.reader(dest_f, delimiter = ',')
        next(data_iter)
        data_types = next(data_iter)
        roles = next(data_iter)
        data = [data for data in data_iter]
    data_array = np.array(data, dtype = float)

    return data_array, data_types, roles


def split_data(array, types, roles):

    numeric = []
    nominal = []
    for row in array:
        numeric_row = []
        nominal_row = []
        for i in range(len(row) - 1):
            if roles[i] == 'label' or roles[i] == 'id':
                numeric_row.append(row[i])
                nominal_row.append(row[i])
            elif types[i] == "numeric":
                numeric_row.append(row[i])
            else:
                nominal_row.append(row[i])

        numeric.append(numeric_row)
        nominal.append(nominal_row)

    return np.array(numeric), np.array(nominal)



data, types, roles = read_csv("tables/final_table.csv")
numeric, nominal = split_data(data, types, roles)

#training and test data for nominal models
x_train, x_test, y_train, y_test = train_test_split(nominal[:, 2:], nominal[:, 1], test_size=.3, random_state=0)

bayes_nominal = NaiveBayes()
bayes_nominal.fit(x_train, y_train)
numeric_prediction = bayes_nominal.predict(x_test, y_test)
print("Accuracy Gaussian Bayes: " + str(bayes_nominal.get_accuracy()))

#training and test data for numeric models
x_train, x_test, y_train, y_test = train_test_split(numeric[:, 2:], numeric[:, 1], test_size=.3, random_state=0)

bayes_gaussian = GaussianNaiveBayes()
bayes_gaussian.fit(x_train, y_train)
numeric_prediction = bayes_gaussian.predict(x_test, y_test)
print("Accuracy Gaussian Bayes: " + str(bayes_gaussian.get_accuracy()))

#logistic regression
regression = LogisticRegression()
regression.fit(x_train, y_train)
regressionPrediction = regression.predict(x_test, y_test)
print("Accuracy Logistic Regression: " + str(regression.get_accuracy()))

#reduce data_set for svc
x_train, x_test, y_train, y_test = train_test_split(numeric[:10000, 2:], numeric[:10000, 1], test_size=.3, random_state=0)
"""
#Support Vector Classification
svc = SVC()
svc.fit(x_train, y_train)
scv_prediction = svc.predict(x_test, y_test)
print("Accuracy SVC: " + str(svc.get_accuracy()))
"""
#print base rate
print("Base rate: " + str(regression.get_base_rate()))

#plot roc curves
fpr, tpr, auc = bayes_nominal.get_roc()
plot_roc(fpr, tpr, auc, "Bayes Nominal")
fpr, tpr, auc = bayes_gaussian.get_roc()
plot_roc(fpr, tpr, auc, "Bayes Gaussian")
fpr, tpr, auc = regression.get_roc()
plot_roc(fpr, tpr, auc, "Logistic Regression")
"""
fpr, tpr, auc = svc.get_roc()
plot_roc(fpr, tpr, auc)
"""