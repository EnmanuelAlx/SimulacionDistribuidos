import numpy as np # importando numpy

class Normal:

    def __init__(self, mu=2, sigma = 1):
        self._mu = mu
        self._sigma = sigma

    def generateProb(self):
        return np.random.normal(self._mu, self._sigma, 1)[0]

