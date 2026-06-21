import tkinter as tk
from tkinter import ttk, messagebox

def calc_movement(path):
    return sum(abs(path[i] - path[i+1]) for i in range(len(path) - 1))
