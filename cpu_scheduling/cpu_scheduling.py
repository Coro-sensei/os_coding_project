import os 
import time 
import sys

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