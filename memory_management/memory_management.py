import tkinter as tk
from tkinter import messagebox

class MemoryGUIMilestone2:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Memory Visualizer - Milestone 2")
        self.os_size = 10  
        self.queue = []
        self.memory_blocks = [] 
        self.process_counter = 1  
        self.setup_gui()

    def setup_gui(self):
        # [UI setup identical to Milestone 1 for structural consistency]
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
        tk.Button(left_frame, text="1. Initialize System", command=self.setup_memory, bg="#d1d1d1").pack(fill=tk.X, pady=2)
        tk.Button(left_frame, text="2. Allocate Next Process", command=self.allocate_next, bg="#a2c2e8").pack(fill=tk.X, pady=2)
        tk.Frame(left_frame, height=2, bd=1, relief="sunken").pack(fill=tk.X, pady=10)
        tk.Label(left_frame, text="Terminate Process (e.g., P1):", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        term_frame = tk.Frame(left_frame)
        term_frame.pack(fill=tk.X, pady=(2, 5))
        self.entry_terminate = tk.Entry(term_frame, width=10)
        self.entry_terminate.pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(term_frame, text="3. Free Memory", command=self.terminate_process, bg="#ffe29a").pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(left_frame, text="Reset System", command=self.reset_all, bg="#fca1a1").pack(fill=tk.X, pady=(15, 5))
        tk.Label(left_frame, text="Activity History Log:", font=("Arial", 9, "italic")).pack(anchor=tk.W, pady=(10, 0))
        log_frame = tk.Frame(left_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)
        self.log_scrollbar = tk.Scrollbar(log_frame)
        self.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_box = tk.Listbox(log_frame, width=38, height=10, font=("Courier", 9), yscrollcommand=self.log_scrollbar.set)
        self.log_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_scrollbar.config(command=self.log_box.yview)
        right_frame = tk.Frame(self.root, padx=15, pady=15)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        tk.Label(right_frame, text="Physical Memory Map", font=("Arial", 11, "bold")).pack(pady=(0, 5))
        self.canvas = tk.Canvas(right_frame, width=220, height=500, bg="#fcfcfc", relief="solid", borderwidth=1)
        self.canvas.pack()

    def log(self, message):
        self.log_box.insert(tk.END, message)
        self.log_box.yview(tk.END)

    def reset_all(self):
        self.canvas.delete("all")
        self.log_box.delete(0, tk.END)
        self.entry_parts.delete(0, tk.END)
        self.entry_parts.insert(0, "10 6 4 4")
        self.entry_queue.delete(0, tk.END)
        self.entry_queue.insert(0, "2 3 4 5 6")
        self.queue = []
        self.memory_blocks = []
        self.process_counter = 1
        self.log("System reset complete.")

    # --- CORE IMPLEMENTATION FOR MILESTONE 2 ---
    def setup_memory(self):
        self.log_box.delete(0, tk.END)
        self.process_counter = 1
        
        try:
            raw_queue = self.entry_queue.get().split()
            self.queue = [int(x) for x in raw_queue]
            if any(val <= 0 for val in self.queue): raise ValueError()
        except ValueError:
            messagebox.showerror("Invalid Input", "Queue must contain positive numbers.")
            return
            
        self.memory_blocks = []
        arch = self.arch_var.get()
        
        try:
            raw_parts = self.entry_parts.get().split()
            parsed_parts = [int(x) for x in raw_parts]
            if not parsed_parts or any(val <= 0 for val in parsed_parts): raise ValueError()
        except ValueError:
            messagebox.showerror("Invalid Input", "Memory sizes must be positive numbers.")
            return

        if arch == "MFT":
            for p_size in parsed_parts:
                self.memory_blocks.append({"size": p_size, "is_free": True, "process": "", "pid": ""})
            self.log("MFT Loaded Successfully.")
        elif arch == "MVT":
            user_space = parsed_parts[0]
            self.memory_blocks.append({"size": user_space, "is_free": True, "process": "", "pid": ""})
            self.log(f"MVT Loaded. Free User Space: {user_space}KB")
            
        self.draw_memory()

    def draw_memory(self):
        self.canvas.delete("all")
        if not self.memory_blocks: return
            
        total_memory = self.os_size + sum(b["size"] for b in self.memory_blocks)
        canvas_height = self.canvas.winfo_height()
        if canvas_height <= 1: canvas_height = 500
            
        usable_height = canvas_height - 20 
        current_y = 10
        canvas_width_left, canvas_width_right = 15, 205
        
        num_items = 1 + len(self.memory_blocks)
        min_height = 25  
        
        heights = []
        remaining_height = usable_height - (num_items * min_height)
        
        if remaining_height > 0 and total_memory > 0:
            os_h = min_height + (self.os_size / total_memory) * remaining_height
            heights.append(os_h)
            for block in self.memory_blocks:
                bh = min_height + (block["size"] / total_memory) * remaining_height
                heights.append(bh)
        else:
            for _ in range(num_items):
                heights.append(min_height)
        
        # Draw OS
        os_pixel_height = heights[0]
        self.canvas.create_rectangle(canvas_width_left, current_y, canvas_width_right, current_y + os_pixel_height, fill="#ff9494", outline="black")
        self.canvas.create_text(110, current_y + (os_pixel_height / 2), text=f"OS ({self.os_size}KB)", font=("Arial", 9, "bold"))
        current_y += os_pixel_height
        
        # Draw Memory Blocks
        for idx, block in enumerate(self.memory_blocks):
            block_pixel_height = heights[idx + 1]
            if block["is_free"]:
                self.canvas.create_rectangle(canvas_width_left, current_y, canvas_width_right, current_y + block_pixel_height, fill="#e0e0e0", outline="black", dash=(4, 4))
                self.canvas.create_text(110, current_y + (block_pixel_height / 2), text=f"Free Hole\n({block['size']}KB)", fill="#555555", justify=tk.CENTER)
            current_y += block_pixel_height

    def allocate_next(self): pass
    def terminate_process(self): pass

if __name__ == "__main__":
    window = tk.Tk()
    app = MemoryGUIMilestone2(window)
    window.mainloop()