import numpy as np


class Ride:
    """
    Represents a ride
    """

    def __init__(self, start, dest, start_time, length):
        self.start = start
        self.destination = dest
        self.start_time = start_time
        self.length = length

    def __repr__(self):
        return f"Ride from {self.start} to {self.destination}; time ({self.start_time}, {self.start_time + self.length})"


class Station:
    """
    Represents a station with docks, standard bikes, ebikes
    Note that bikes and docks are treated as indistinguishable (only keep track of the counts, not the specific docks)
    """

    def __init__(self, num_docks, num_sbikes, num_ebikes, res_limit):
        self.num_docks = num_docks
        self.num_sbikes = num_sbikes
        self.num_ebikes = num_ebikes
        self.res_limit = res_limit

        self.n_sreserved = 0
        self.n_ereserved = 0

    def __repr__(self):
        return f"Station: ({self.num_sbikes}, {self.n_sreserved}) SBikes, ({self.num_ebikes}, {self.n_ereserved}) EBikes"

    def check_out(self, btype, can_convert_ebikes=False):
        """
        Check out a bike & update station
        Returns True if successful and False if none available
        """
        assert btype == "SBIKE" or btype == "EBIKE"

        if btype == "SBIKE":
            if self.num_sbikes > 0 and self.num_sbikes > self.n_sreserved:
                self.num_sbikes -= 1
                return True
            elif can_convert_ebikes and self.num_ebikes > 0 and self.num_ebikes > self.n_ereserved:
                # convert an ebike to sbike
                self.num_ebikes -= 1
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
        """
        Attempts to return a bike & updates station
        Returns True if successful and False if none available
        """
        assert btype == "SBIKE" or btype == "EBIKE"

        # create a random video file size that should begin transferring to the kiosk upon return
        video_file = create_random_video_size()

        if self.num_sbikes + self.num_ebikes < self.num_docks:
            if btype == "SBIKE":
                self.num_sbikes += 1
            else:
                self.num_ebikes += 1

            # begin transferring the video at the USB 3.1 transfer rate of 600MB/s
            time_to_complete_transfer = video_file / 600

            return True
        else:
            return False

    def reserve_bike(self, btype):
        """
        Attempt to reserve a bike of a certain type
        Returns True if successful and False if none available or at reservation limit
        """
        assert btype == "SBIKE" or btype == "EBIKE"

        # check if we've exceeded reservation limit
        if self.n_sreserved + self.n_ereserved >= self.res_limit:
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
    """
    Sample an integer from a normal distribution, with an optional min value
    """
    if floor:
        return max(floor, int(np.random.normal(mean, std) + 0.5))
    else:
        return int(np.random.normal(mean, std) + 0.5)


def create_random_video_size(minimum_file_size=45, max_file_size=128_000):
    """
    Returns a random video file size in MB between min_file_size and max_file_size
    """
    return np.random.randint(minimum_file_size, max_file_size)
