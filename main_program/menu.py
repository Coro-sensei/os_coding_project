import tkinter as tk
import sys
import os

# Project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))

# Add folders
folders = [
    "cpu_scheduling",
    "memory_management",
    "mass_storage_management",
    "virtual_memory"
]

for folder in folders:
    sys.path.insert(0, os.path.join(project_root, folder))

# Imports
import cpu_scheduling
import memory_management
sys.path.append(os.path.join(project_root, "mass_storage_management"))
import mass_storage
import main as virtual_memory


# Run CPU Scheduling
def run_cpu():
    cpu_scheduling.main()


# Run Memory Management
def run_memory():
    memory_management.main()


# Run Mass Storage Management
def run_storage():
    mass_storage.main()


# Run Virtual Memory
def run_virtual():
    virtual_memory.main()


# Main menu
root = tk.Tk()
root.title("Operating System Simulator")
root.geometry("500x450")
root.resizable(False, False)

# Title
tk.Label(
    root,
    text="Operating System Simulator",
    font=("Arial", 18, "bold")
).pack(pady=20)

# Buttons
tk.Button(root, text="CPU Scheduling", width=30, height=2, command=run_cpu).pack(pady=10)
tk.Button(root, text="Memory Management", width=30, height=2, command=run_memory).pack(pady=10)
tk.Button(root, text="Mass Storage Management", width=30, height=2, command=run_storage).pack(pady=10)
tk.Button(root, text="Virtual Memory", width=30, height=2, command=run_virtual).pack(pady=10)

tk.Button(root, text="Exit", width=30, height=2, command=root.quit).pack(pady=20)

root.mainloop()