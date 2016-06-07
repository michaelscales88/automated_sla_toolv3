# Call ID class which gathers information from Chronicall report to be collated
# Hold/Park/Transfer times used in calculating True Hold duration for answered calls
from .utils import (convert_time_stamp)


class CallId:

    def __init__(self, name):
        self.name = name
        self.total_hold_time = 0
        self.hold = 0
        self.transfer_hold = 0
        self.park = 0

    def __str__(self):
        print(self.name)
        print("total_hold_time: %s" % convert_time_stamp(self.total_hold_time))
        print("hold time: %s" % convert_time_stamp(self.hold))
        print("transfer_hold time: %s" % convert_time_stamp(self.transfer_hold))
        print("Park Time: %s" % convert_time_stamp(self.park))
        
    def set_total_hold_time(self):
        self.total_hold_time = self.hold + self.transfer_hold + self.park
        
    def set_hold(self, hold_time):
        self.hold += hold_time
        
    def set_transfer_hold(self, transfer_hold_time):
        self.transfer_hold += transfer_hold_time
        
    def set_park(self, park_time):
        self.park += park_time        

    def get_total_hold_time(self):
        return self.total_hold_time

    def get_name(self):
        return self.name
