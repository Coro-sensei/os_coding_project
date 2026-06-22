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

def note(msg):
    print(C.bblack + msg + C.reset)

def error(msg):
    print(C.bred + msg + C.reset)
# Gantt chart:

def draw_gantt(timeline):
    """"timeline: list of (pid, start_time, end_time)"""
    section("Gantt Chart")
    if not timeline:
        note("No processes were scheduled.")
        return
    
    total = timeline[-1][2]  # end_time of last entry
    max_w = WIDTH - 4
    scale = max(1, total / max_w) if total > max_w else 1
    widths = [max(1, round((e - s) / scale)) for _, s, e in timeline]

    top = " ┌" + "".join("─" * w + "┬" for w in widths)
    print(top[:-1] + "┐")

    row = " │"
    for (pid, s, e), w in zip(timeline, widths):
        label =(pid or 'IDLE').center(w)[:w]
        row += proc_color(pid) + label + C.reset + "│"
    print(row)

    bot =  "  └" + "".join("─" * w + "┴" for w in widths)
    print(bot[:-1] + "┘")

    labels =  "  " + "".join(str(s).ljust(w) for (_, s, _), w in zip(timeline, widths))
    print(C.bblack+labels + C.reset)
    print()


# Results table

def draw_results(processes):
    section("Process Results")
    hdr = (f"  {'PID':<6}{'Arrival':<10}{'Burst':<8}" f"{'Finish':<10}{'Turnaround':<13}{'Waiting':<10}{'Response':<10}")
    print(C.bold +C.bwhite + hdr + C.reset)
    hr('-', C.bwhite)
    tot_ta = tot_wt = tot_rt = 0
    for p in sorted(processes, key=lambda x: x.pid):
        col = proc_color(p.pid)
        pid_str = col + C.BOLD + f" {p.pid}" + C.RESET
        print(f"  {pid_str:<20}{p.arrival:<10}{p.burst:<8}"
            f"{p.finish_time:<10}{p.turnaround_time:<13}"
            f"{p.waiting_time:<10}{p.response_time:<10}")
        tot_ta += p.turnaround_time
        tot_wt += p.waiting_time
        tot_rt += p.response_time

    n = len(processes)
    hr("·", C.BBLACK)
    avg_ta = tot_ta / n
    avg_wt = tot_wt / n
    avg_rt = tot_rt / n
    print(f"  {C.BOLD}{'Averages':<6}{'':<10}{'':<8}{'':<10}"
        f"{avg_ta:<13.2f}{avg_wt:<10.2f}{avg_rt:<10.2f}{C.RESET}")
    print()
    return avg_wt, avg_ta, avg_rt

# Finish calculations
def finalise(processes):
    for p in processes:
        p.turnaround_time = p.finish_time - p.arrival
        p.waiting_time    = p.turnaround_time - p.burst
        if p.response_time is None:
            p.response_time = p.waiting_time
if __name__ == "__main__":
    main()