class FluctuatingValue(object):
    def __init__(self, initial_val, low_val=None, hi_val=None, fluctuate=False, function=None):
        self.fluctuateOn = fluctuate
        self.current_val = initial_val
        self.low_val = low_val
        self.hi_val = hi_val

        '''
        function should be a lambda, like `lambda frac, whole: frac * whole`
        '''
        self.function = function

    def fluctuate(self, fraction=None):
        if self.fluctuateOn:
            diff = self.hi_val - self.low_val
            self.current_val = self.low_val + self.function(fraction, diff)

    def get(self):
        return self.current_val
