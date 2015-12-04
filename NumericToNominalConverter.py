__author__ = 'flo'
import numpy as np

class NumericToNominalConverter:

    def __init__(self, data, num_bins = 3, type = 'uniform'):
        self.data = data
        self.num_bins = num_bins
        self.type = type
        self.converter_type = {'uniform': self.convert_uniform}

    def convert(self):
        if self.type in self.converter_type:
            return self.converter_type[self.type]()
        else:
            print("Convertion type: " + self.type + " not valid!")
            exit(1)

    def convert_uniform(self):
        hist, bin_edges = np.histogram(self.data.astype(np.float), bins=self.num_bins)
        print(bin_edges)