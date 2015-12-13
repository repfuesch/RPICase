import hashlib

"""
This class represents a pair of objects that can be used in a dictionary to uniquely identify
the pair, such that key(a, b) = key(b ,a)
"""

class SymmetricPair:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return (self.a == other.a and self.b == other.b) or (self.a == other.b and self.b == other.a)

    def __hash__(self):
        h1 = hashlib.sha256(str(self.a).encode())
        h2 = hashlib.sha256(str(self.b).encode())
        key = int(h1.hexdigest(), 16) & int(h2.hexdigest(), 16)
        return key