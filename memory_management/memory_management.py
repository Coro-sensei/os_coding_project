import tkinter as tk
from tkinter import messagebox

class MemoryGUIMilestone1:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Memory Visualizer - Memory Management")
        
        # --- CONFIGURATION VARIABLES ---
        self.os_size = 10  
        self.queue = []
        self.memory_blocks = [] 
        self.process_counter = 1  
        
        self.setup_gui()

    def setup_gui(self):
        # LEFT PANEL: Controls & Inputs
        left_frame = tk.Frame(self.root, padx=15, pady=15)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(left_frame, text="Memory Architecture:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.arch_var = tk.StringVar(value="MFT")
        arch_menu = tk.OptionMenu(left_frame, self.arch_var, "MFT", "MVT")
        arch_menu.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(left_frame, text="Allocation Policy:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.algo_var = tk.StringVar(value="Best Fit")
        algo_menu = tk.OptionMenu(left_frame, self.algo_var, "First Fit", "Best Fit", "Best Available Fit")
        algo_menu.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(left_frame, text="MFT Partitions OR MVT Total Space:", font=("Arial", 9)).pack(anchor=tk.W)
        self.entry_parts = tk.Entry(left_frame, width=30)
        self.entry_parts.insert(0, "10 6 4 4")
        self.entry_parts.pack(pady=(0, 10))
        
        tk.Label(left_frame, text="Process Input Queue:", font=("Arial", 9)).pack(anchor=tk.W)
        self.entry_queue = tk.Entry(left_frame, width=30)
        self.entry_queue.insert(0, "2 3 4 5 6") 
        self.entry_queue.pack(pady=(0, 15))
        
        # Action Buttons
        tk.Button(left_frame, text="1. Initialize System", command=self.setup_memory, bg="#d1d1d1").pack(fill=tk.X, pady=2)
        tk.Button(left_frame, text="2. Allocate Next Process", command=self.allocate_next, bg="#a2c2e8").pack(fill=tk.X, pady=2)
        
        # Deallocation Section
        tk.Frame(left_frame, height=2, bd=1, relief="sunken").pack(fill=tk.X, pady=10)
        tk.Label(left_frame, text="Terminate Process (e.g., P1):", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        
        term_frame = tk.Frame(left_frame)
        term_frame.pack(fill=tk.X, pady=(2, 5))
        self.entry_terminate = tk.Entry(term_frame, width=10)
        self.entry_terminate.pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(term_frame, text="3. Free Memory", command=self.terminate_process, bg="#ffe29a").pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(left_frame, text="Reset System", command=self.reset_all, bg="#fca1a1").pack(fill=tk.X, pady=(15, 5))
        
        # Activity History Log Box
        tk.Label(left_frame, text="Activity History Log:", font=("Arial", 9, "italic")).pack(anchor=tk.W, pady=(10, 0))
        log_frame = tk.Frame(left_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)
        self.log_scrollbar = tk.Scrollbar(log_frame)
        self.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_box = tk.Listbox(log_frame, width=38, height=10, font=("Courier", 9), yscrollcommand=self.log_scrollbar.set)
        self.log_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_scrollbar.config(command=self.log_box.yview)

        # RIGHT PANEL: Graphical Map Display
        right_frame = tk.Frame(self.root, padx=15, pady=15)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        tk.Label(right_frame, text="Physical Memory Map", font=("Arial", 11, "bold")).pack(pady=(0, 5))
        self.canvas = tk.Canvas(right_frame, width=220, height=500, bg="#fcfcfc", relief="solid", borderwidth=1)
        self.canvas.pack()

    # --- PLACEHOLDER FUNCTIONS FOR MILESTONE 1 ---
    def log(self, message):
        self.log_box.insert(tk.END, message)
        self.log_box.yview(tk.END)

    def setup_memory(self):
        self.log("Button 1 Clicked: Initialize System (Stub)")

    def allocate_next(self):
        self.log("Button 2 Clicked: Allocate Next Process (Stub)")

    def terminate_process(self):
        self.log("Button 3 Clicked: Free Memory (Stub)")

    def reset_all(self):
        self.log_box.delete(0, tk.END)
        self.log("System reset stub triggered.")

if __name__ == "__main__":
    window = tk.Tk()
    app = MemoryGUIMilestone1(window)
    window.mainloop()