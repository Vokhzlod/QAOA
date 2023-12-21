import numpy as np


class Statistic:
    """
    See: https://fanf2.user.srcf.net/hermes/doc/antiforgery/stats.pdf
    """

    def __init__(self, cvar=1):
        self.cvar = cvar
        self.reset()

    def reset(self):
        self.W = 0
        self.maxval = float("-inf")
        self.minval = float("inf")
        self.minSols = []
        self.maxSols = []
        self.E = 0
        self.S = 0
        self.all_values = np.array([])

    def add_sample(self, value, weight, string):
        self.W += weight
        tmp_E = self.E
        if value >= self.maxval:
            if value == self.maxval:
                self.maxSols.append(string)
            else:
                self.maxval = value
                self.maxSols = [string]
        if value <= self.minval:
            if value == self.minval:
                self.minSols.append(string)
            else:
                self.minval = value
                self.minSols = [string]

        self.maxval = max(value, self.maxval)
        self.minval = min(value, self.minval)
        self.E += weight / self.W * (value - self.E)
        self.S += weight * (value - tmp_E) * (value - self.E)        
        if self.cvar < 1:
            idx = np.searchsorted(self.all_values, value)
            self.all_values = np.insert(
                self.all_values, idx, np.ones(int(weight)) * value
            )

    def get_E(self):
        return self.E

    def get_Variance(self):
        return self.S / (self.W - 1)

    def get_max(self):
        return self.maxval

    def get_min(self):
        return self.minval
    
    def get_max_sols(self):
        return self.maxSols
    
    def get_min_sols(self):
        return self.minSols

    def get_CVaR(self):
        if self.cvar < 1:
            cvarK = int(np.round(self.cvar * len(self.all_values)))
            cvar = np.sum(self.all_values[-cvarK:]) / cvarK
            return cvar
        else:
            return self.get_E()
