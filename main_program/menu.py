#create a menu to select all the options on what program (cpu scheduling, memory management, mass storage, virtual memory) to run, with gui. 

import tkinter as tk
import sys
import os

# Ensure parent directory is on sys.path so sibling modules can be imported
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import your program files (if they are missing, show a clear ImportError)
try:
    import cpu_scheduling
    import memory_management
    import mass_storage_management
    import virtual_memory
except Exception as e:
    tk.messagebox = tk.messagebox if hasattr(tk, 'messagebox') else None
    print(f"Failed to import module: {e}")
    # Allow GUI to start even if imports fail



# Functions to launch each program
def run_cpu():
    try:
        cpu_scheduling.main()
    except NameError:
        tk.messagebox.showerror("Error", "CPU Scheduling module not loaded")

def run_memory():
    try:
        memory_management.main()
    except NameError:
        tk.messagebox.showerror("Error", "Memory Management module not loaded")

def run_storage():
    try:
        mass_storage_management.main()
    except NameError:
        tk.messagebox.showerror("Error", "Mass Storage Management module not loaded")

def run_virtual():
    try:
        virtual_memory.main()
    except NameError:
        tk.messagebox.showerror("Error", "Virtual Memory module not loaded")


# Main menu window
root = tk.Tk()
root.title("OS Management System")
root.geometry("400x350")


# Title label
title = tk.Label(root, text="Operating System Simulator", font=("Arial", 16, "bold"))
title.pack(pady=20)


# Buttons for each program
btn_cpu = tk.Button(root, text="CPU Scheduling", width=25, height=2, command=run_cpu)
btn_cpu.pack(pady=10)

btn_memory = tk.Button(root, text="Memory Management", width=25, height=2, command=run_memory)
btn_memory.pack(pady=10)

btn_storage = tk.Button(root, text="Mass Storage Management", width=25, height=2, command=run_storage)
btn_storage.pack(pady=10)

btn_virtual = tk.Button(root, text="Virtual Memory", width=25, height=2, command=run_virtual)
btn_virtual.pack(pady=10)


# Exit button
exit_btn = tk.Button(root, text="Exit", width=25, height=2, command=root.quit)
exit_btn.pack(pady=20)


root.mainloop()