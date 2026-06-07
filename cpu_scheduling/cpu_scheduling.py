from cProfile import label
import os 
from pydoc import text
import time 
import sys
from timeit import main

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

    # Background
    bg_black = '\033[40m'
    bg_red = '\033[41m'
    bg_green = '\033[42m'
    bg_yellow = '\033[43m'  
    bg_blue = '\033[44m'
    bg_magenta = '\033[45m'
    bg_cyan = '\033[46m'
    bg_white = '\033[47m'

process_colors = [
    C.bg_blue + C.bwhite,
    C.bg_green + C.bblack,
    C.bg_yellow + C.bblack,
    C.bg_magenta + C.bwhite,
    C.bg_cyan + C.bblack,
    C.bg_red + C.bwhite,
    C.bg_white + C.bblack,
]

idle_color = C.dim + C.bblack

def proc_color(pid):
    if pid is None:
        return idle_color
    idx = int(pid[1:]) - 1
    return process_colors[idx % len(process_colors)] 

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

def hr(char = '-', color  = C.bblack):
    print(color + char * WIDTH + C.reset)

def banner(text, color = C.cyan):
    print()
    hr('=', color)
    pad = (WIDTH - len(text) - 2) // 2
    print(color + ' ' * pad + text + ' ' * pad + C.reset)
    hr('=', color)
    print()

def section(text):
    print()
    hr('-', C.bblack)
    print(C.bold + text + C.reset)
    hr('-', C.bblack)

def info(label, value, lw = 20):
    print(f"  {C.dim}{label:<{lw}}{C.reset}{C.bold}{value}{C.reset}")

def success(msg):
    print(C.green + msg + C.reset)

def error(msg):
    print(C.bred + msg + C.reset)
# Gantt chart:

def draw_gantt(timeline):
    """"timeline: list of (pid, start_time, end_time)"""
    section("Gantt Chart")
    if not timeline:
        


if __name__ == "__main__":
    main()