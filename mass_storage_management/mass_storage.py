import tkinter as tk
from tkinter import ttk, messagebox

def calc_movement(path):
    return sum(abs(path[i] - path[i+1]) for i in range(len(path) - 1))

def calculate_fcfs(queue, head):
    path = [head] + queue
    return path, calc_movement(path)

def calculate_sstf(queue, head):
    path = [head]
    unvisited = queue.copy()
    current = head
    while unvisited:
        closest = min(unvisited, key=lambda x: abs(x - current))
        path.append(closest)
        unvisited.remove(closest)
        current = closest
    return path, calc_movement(path)

def calculate_scan(queue, head, max_track=199):
    path = [head]
    left = sorted([x for x in queue if x < head])
    right = sorted([x for x in queue if x >= head])

    path.extend(right)
    if right and right[-1] != max_track:
        path.append(max_track)
    path.extend(reversed(left))
    return path, calc_movement(path)

def calculate_cscan(queue, head, max_track=199):
    path = [head]
    left = sorted([x for x in queue if x < head])
    right = sorted([x for x in queue if x >= head])

    path.extend(right)
    path.append(max_track)
    path.append(0)
    path.extend(left)
    return path, calc_movement(path)

def calculate_look(queue, head):
    path = [head]
    left = sorted([x for x in queue if x < head])
    right = sorted([x for x in queue if x >= head])

    path.extend(right)
    path.extend(reversed(left))
    return path, calc_movement(path)

def calculate_clook(queue, head):
    path = [head]
    left = sorted([x for x in queue if x < head])
    right = sorted([x for x in queue if x >= head])

    path.extend(right)
    path.extend(left)
    return path, calc_movement(path)

def draw_graph(path):
    canvas.delete("all")
    if not path: return

    c_width, c_height = 550, 350
    pad_x, pad_y = 20, 20

    max_track = max(max(path), 199)

    points = []
    for index, track in enumerate(path):
        x = pad_x + (track / max_track) * (c_width - 2 * pad_x)
        y = pad_y + (index / max(1, len(path) - 1)) * (c_height - 2 * pad_y)
        points.append((x, y))