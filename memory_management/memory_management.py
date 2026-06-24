import tkinter as tk
from tkinter import messagebox

class CompleteMemoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Memory Visualizer - Milestone 4 (Final)")
        self.os_size = 10  
        self.queue = []
        self.memory_blocks = [] 
        self.process_counter = 1  
        self.setup_gui()

    def setup_gui(self):
        # [UI elements remain identical]
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

    def update_queue_textbox(self):
        self.entry_queue.delete(0, tk.END)
        self.entry_queue.insert(0, " ".join(str(p) for p in self.queue))

    def reset_all(self):
        self.canvas.delete("all")
        self.log_box.delete(0, tk.END)
        self.entry_parts.delete(0, tk.END)
        self.entry_parts.insert(0, "10 6 4 4")
        self.entry_queue.delete(0, tk.END)
        self.entry_queue.insert(0, "2 3 4 5 6")
        self.entry_terminate.delete(0, tk.END)
        self.queue = []
        self.memory_blocks = []
        self.process_counter = 1
        self.log("System reset complete.")

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

    def allocate_next(self):
        if not self.memory_blocks:
            messagebox.showwarning("System Not Ready", "Please click 'Initialize System' first!")
            return
        if not self.queue:
            messagebox.showinfo("Complete", "No processes remaining in the queue!")
            return
            
        process_size = self.queue.pop(0)
        algo = self.algo_var.get()
        arch = self.arch_var.get()
        chosen_index = -1
        
        if arch == "MFT":
            if algo == "First Fit":
                for i in range(len(self.memory_blocks)):
                    if self.memory_blocks[i]["is_free"] and self.memory_blocks[i]["size"] >= process_size:
                        chosen_index = i
                        break
            elif algo == "Best Fit":
                closest_match_diff = float('inf')
                target_slot = -1
                for i in range(len(self.memory_blocks)):
                    if self.memory_blocks[i]["size"] >= process_size:
                        diff = self.memory_blocks[i]["size"] - process_size
                        if diff < closest_match_diff:
                            closest_match_diff = diff
                            target_slot = i
                        elif diff == closest_match_diff:
                            if target_slot == -1 or (not self.memory_blocks[target_slot]["is_free"] and self.memory_blocks[i]["is_free"]):
                                target_slot = i
                if target_slot != -1 and self.memory_blocks[target_slot]["is_free"]:
                    chosen_index = target_slot
            elif algo == "Best Available Fit":
                closest_match_diff = float('inf')
                for i in range(len(self.memory_blocks)):
                    if self.memory_blocks[i]["is_free"] and self.memory_blocks[i]["size"] >= process_size:
                        diff = self.memory_blocks[i]["size"] - process_size
                        if diff < closest_match_diff:
                            closest_match_diff = diff
                            chosen_index = i
                            
        elif arch == "MVT":
            if algo == "First Fit":
                for i in range(len(self.memory_blocks)):
                    if self.memory_blocks[i]["is_free"] and self.memory_blocks[i]["size"] >= process_size:
                        chosen_index = i
                        break
            elif algo in ["Best Fit", "Best Available Fit"]:
                closest_match_diff = float('inf')
                for i in range(len(self.memory_blocks)):
                    if self.memory_blocks[i]["is_free"] and self.memory_blocks[i]["size"] >= process_size:
                        diff = self.memory_blocks[i]["size"] - process_size
                        if diff < closest_match_diff:
                            closest_match_diff = diff
                            chosen_index = i

        if chosen_index != -1:
            target_block = self.memory_blocks[chosen_index]
            pid_str = f"P{self.process_counter}"
            self.process_counter += 1
            
            if arch == "MFT":
                target_block["is_free"] = False
                target_block["pid"] = pid_str
                target_block["process"] = f"{pid_str} ({process_size}KB)"
                wasted = target_block["size"] - process_size
                self.log(f"Allocated {pid_str}({process_size}K). Int Frag: {wasted}K")
            elif arch == "MVT":
                leftover_hole = target_block["size"] - process_size
                target_block["is_free"] = False
                target_block["size"] = process_size
                target_block["pid"] = pid_str
                target_block["process"] = f"{pid_str} ({process_size}KB)"
                if leftover_hole > 0:
                    self.memory_blocks.insert(chosen_index + 1, {"size": leftover_hole, "is_free": True, "process": "", "pid": ""})
                self.log(f"Allocated {pid_str}({process_size}K). Split Leftover: {leftover_hole}K")
        else:
            self.queue.append(process_size)
            self.log(f"SKIPPED Process size {process_size}KB -> Sent to back.")
            
        self.update_queue_textbox()
        self.draw_memory()

    # --- CORE IMPLEMENTATION FOR MILESTONE 4 ---
    def terminate_process(self):
        target_pid = self.entry_terminate.get().strip().upper()
        if not target_pid:
            messagebox.showwarning("Input Missing", "Please enter a process ID to terminate (e.g., P1).")
            return
            
        found = False
        for block in self.memory_blocks:
            if not block["is_free"] and block["pid"] == target_pid:
                block["is_free"] = True
                block["process"] = ""
                block["pid"] = ""
                found = True
                break
                
        if found:
            self.log(f"Process {target_pid} terminated successfully.")
            if self.arch_var.get() == "MVT":
                self.merge_adjacent_mvt_holes()
            self.entry_terminate.delete(0, tk.END)
            self.draw_memory()
        else:
            messagebox.showwarning("Not Found", f"Process '{target_pid}' is not currently loaded in memory.")

    def merge_adjacent_mvt_holes(self):
        i = 0
        merges_occurred = 0
        while i < len(self.memory_blocks) - 1:
            if self.memory_blocks[i]["is_free"] and self.memory_blocks[i+1]["is_free"]:
                self.memory_blocks[i]["size"] += self.memory_blocks[i+1]["size"]
                self.memory_blocks.pop(i+1)
                merges_occurred += 1
            else:
                i += 1
        if merges_occurred > 0:
            self.log(f"MVT Coalescing Engine triggered: Merged adjacent free memory holes.")

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
            for _ in range(num_items): heights.append(min_height)
            
        os_pixel_height = heights[0]
        self.canvas.create_rectangle(canvas_width_left, current_y, canvas_width_right, current_y + os_pixel_height, fill="#ff9494", outline="black")
        self.canvas.create_text(110, current_y + (os_pixel_height / 2), text=f"OS ({self.os_size}KB)", font=("Arial", 9, "bold"))
        current_y += os_pixel_height
        
        for idx, block in enumerate(self.memory_blocks):
            block_pixel_height = heights[idx + 1]
            if block["is_free"]:
                self.canvas.create_rectangle(canvas_width_left, current_y, canvas_width_right, current_y + block_pixel_height, fill="#e0e0e0", outline="black", dash=(4, 4))
                self.canvas.create_text(110, current_y + (block_pixel_height / 2), text=f"Free Hole\n({block['size']}KB)", fill="#555555", justify=tk.CENTER)
            else:
                self.canvas.create_rectangle(canvas_width_left, current_y, canvas_width_right, current_y + block_pixel_height, fill="#99ccff", outline="black")
                self.canvas.create_text(110, current_y + (block_pixel_height / 2), text=f"{block['process']}\nTotal Size: {block['size']}KB", fill="black", font=("Arial", 9, "bold"), justify=tk.CENTER)
            current_y += block_pixel_height

if __name__ == "__main__":
    window = tk.Tk()
    app = CompleteMemoryGUI(window)
    window.mainloop()