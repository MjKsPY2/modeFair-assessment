import numpy as np


def getEuclideanDistance(point1, point2):
    return 100 * np.linalg.norm(point1 - point2)
