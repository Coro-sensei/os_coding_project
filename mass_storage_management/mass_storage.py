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