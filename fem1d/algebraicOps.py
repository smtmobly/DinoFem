import numpy as np


def direct_inverse(A, b):
    u = np.linalg.inv(A).dot(b)
    return u
