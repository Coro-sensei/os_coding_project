import os 
import time 
import sys

# ANSI color codes:
class C:
    reset = '\033[0m'
    bold = '\033[1m'
    dim = '\033[2m'

    # Foreground
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'
    
    # Bright Foreground
    bblack = '\033[90m'
    bred = '\033[91m'
    bgreen = '\033[92m'
    byellow = '\033[93m'    
    bblue = '\033[94m'
    bmagenta = '\033[95m'
    bcyan = '\033[96m'
    bwhite = '\033[97m'



# Process class:
class Process: 
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0

        # computed
        self.start_time = None
        self.finish_time = None
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = None

    def __repr__(self):
        return (f"Process(pid={self.pid}, arrival_time={self.arrival_time}, "
                f"burst_time={self.burst_time})")
    
# ASCII 

WIDTH = 78

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
