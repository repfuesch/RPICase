__author__ = 'flo'

from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import sklearn.naive_bayes as nb
import sklearn.svm as svm
import sklearn.linear_model.logistic as log

class PredictionModel(object):

    def __init__(self):
        self.y_predicted = []
        self.y_score = []
        self.y_test = []

    def fit(self, x, y):

        self.classifier.fit(x, y)

    def predict(self, x, y):

        self.y_test = y
        self.y_predicted = self.classifier.predict(x)
        return self.y_predicted

    def get_accuracy(self):

        count = 0
        for i in range(len(self.y_test) - 1):
            if self.y_test[i] != self.y_predicted[i]:
                count += 1

        predicted_wrong = count
        accuracy = float(len(self.y_test) - predicted_wrong) / float(len(self.y_test))
        return accuracy

    def get_base_rate(self):

        pos_samples = (self.y_test == 1).sum()
        neg_samples = len(self.y_test) - pos_samples
        if neg_samples > pos_samples:

            return float(neg_samples) / len(self.y_test)

    def get_roc(self):

        fpr, tpr, thresholds = roc_curve(self.y_test, self.y_score)
        area = auc(fpr, tpr)

        return fpr, tpr, area


class NaiveBayes(PredictionModel):

    def __init__(self):
        self.classifier = nb.MultinomialNB()
        super(NaiveBayes, self)

    def predict(self, x, y):
        self.y_score = self.classifier.predict_proba(x)[:, 1]
        return super(NaiveBayes, self).predict(x, y)

class LogisticRegression(PredictionModel):

    def __init__(self):
        self.classifier = log.LogisticRegression()
        super(LogisticRegression, self)

    def predict(self, x, y):
        self.y_score = self.classifier.predict_proba(x)[:, 1]
        return super(LogisticRegression, self).predict(x, y)


# Plot of a ROC curve for one class
def plot_roc(fpr, tpr, auc):
    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()