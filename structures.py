import numpy as np

class Ride:
    def __init__(self, start, dest, start_time, length):
        self.start = start
        self.destination = dest
        self.start_time = start_time
        self.length = length

    def __repr__(self):
        return f"Ride from {self.start} to {self.destination}; time ({self.start_time}, {self.start_time + self.length})"


class Station:
    def __init__(self, num_docks, num_sbikes, num_ebikes, res_limit):
        self.num_docks = num_docks
        self.num_sbikes = num_sbikes
        self.num_ebikes = num_ebikes
        
        self.n_sreserved = 0
        self.n_ereserved = 0
        self.res_limit = res_limit
        

    def check_out(self, btype):
        '''
        Check out a bike & update station
        Returns True if successful and False if none available
        '''
        assert (btype == "SBIKE" or btype == "EBIKE")
        
        if btype == "SBIKE":
            if self.num_sbikes > 0 and self.num_sbikes > self.n_sreserved:
                self.num_sbikes -= 1
                return True
            else:
                return False
        else:
            if self.num_ebikes > 0 and self.num_ebikes > self.n_ereserved:
                self.num_ebikes -= 1
                return True
            else:
                return False

    def return_bike(self, btype):
        '''
        Attempts to return a bike & updates station
        Returns True if successful and False if none available
        '''
        assert (btype == "SBIKE" or btype == "EBIKE")
        
        if self.num_sbikes + self.num_ebikes < self.num_docks:
            if btype == "SBIKE":
                self.num_sbikes += 1
            else:
                self.num_ebikes += 1
            return True
        else:
            return False


    def reserve_bike(self, btype):
        '''
        Attempt to reserve a bike of a certain type
        Returns True if successful and False if none available or at reservation limit
        '''
        assert (btype == "SBIKE" or btype == "EBIKE")

        # check if we've exceeded reservation limit
        if self.n_reserved >= self.res_limit:
            return False

        if btype == "SBIKE":
            if self.num_sbikes > 0 and self.n_sreserved < self.num_sbikes:
                self.n_sreserved += 1
                return True
            else:
                return False
        else:
            if self.num_ebikes > 0 and self.n_ereserved < self.num_ebikes:
                self.n_ereserved += 1
                return True
            else:
                return False


## HELPER FUNCS

def sample_norm_int(mean, std, floor=None):
    '''
    Sample an integer from a normal distribution, with an optional min value
    '''
    if floor:
        return max(floor, int(np.random.normal(mean, std) + 0.5))
    else:
        return int(np.random.normal(mean, std) + 0.5)