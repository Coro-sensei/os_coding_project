import tkinter as tk
from tkinter import messagebox

MAX_REFERENCES = 20
MAX_FRAMES = 10


class CountingBasedSimulator:
	"""
	Counting-Based Page Replacement.

	Keeps a counter per page = how many times it has been referenced so far.
	- On HIT or FAULT-insert: increment that page's counter.
	- On FAULT with frames full, choose a victim among pages in frames:
		LFU (Least Frequently Used) -> evict the page with the SMALLEST counter
		                                (it's been used the least, assume it
		                                won't be needed again soon).
		MFU (Most Frequently Used)  -> evict the page with the LARGEST counter
		                                (argument: it was just used heavily,
		                                so it's "done" and unlikely to be
		                                needed again soon).
	Ties are broken by whichever qualifying page appears first in frames.
	"""

	def __init__(self, root):
		self.root = root
		self.root.title("Counting-Based Page Replacement Simulator")
		self.root.geometry("700x650")

		# Title
		tk.Label(root, text="Counting-Based Page Replacement (LFU / MFU)",
				 font=("Arial", 16, "bold")).pack(pady=10)

		# Frame input
		frame_input = tk.Frame(root)
		frame_input.pack(pady=5)

		tk.Label(frame_input, text=f"Page Frames (1-{MAX_FRAMES}):").grid(row=0, column=0)
		self.frames_entry = tk.Entry(frame_input, width=10)
		self.frames_entry.grid(row=0, column=1)

		# Reference string input
		tk.Label(root, text=f"Reference String (comma-separated, max {MAX_REFERENCES}):").pack()
		self.ref_entry = tk.Entry(root, width=50)
		self.ref_entry.pack(pady=5)

		# Strategy selector (LFU / MFU)
		strategy_frame = tk.Frame(root)
		strategy_frame.pack(pady=5)

		tk.Label(strategy_frame, text="Strategy:").grid(row=0, column=0, padx=5)
		self.strategy_var = tk.StringVar(value="LFU")
		tk.Radiobutton(strategy_frame, text="LFU (evict least frequently used)",
					   variable=self.strategy_var, value="LFU").grid(row=0, column=1, padx=5)
		tk.Radiobutton(strategy_frame, text="MFU (evict most frequently used)",
					   variable=self.strategy_var, value="MFU").grid(row=0, column=2, padx=5)

		# Run button
		tk.Button(root, text="Run Simulation", command=self.run_counting,
				  bg="teal", fg="white").pack(pady=10)

		# Output box
		self.output = tk.Text(root, height=20, width=80)
		self.output.pack(pady=10)

	def run_counting(self):
		self.output.delete("1.0", tk.END)
		strategy = self.strategy_var.get()  # "LFU" or "MFU"

		# Validate frames
		try:
			frames_count = int(self.frames_entry.get())
			if frames_count < 1 or frames_count > MAX_FRAMES:
				raise ValueError
		except ValueError:
			messagebox.showerror("Error", f"Frames must be 1 to {MAX_FRAMES}")
			return

		# Validate reference string
		try:
			ref_string = [int(x.strip()) for x in self.ref_entry.get().split(",") if x.strip() != ""]
			if len(ref_string) < 1 or len(ref_string) > MAX_REFERENCES:
				raise ValueError
		except ValueError:
			messagebox.showerror("Error",
								f"Enter 1 to {MAX_REFERENCES} integers separated by commas")
			return

		frames = []
		counters = {}  # counters[page] = number of times referenced so far
		page_faults = 0
		self.steps_queue = []

		self.output.insert(tk.END, f"Counting-Based ({strategy}) Simulation Steps:\n")
		self.output.insert(tk.END, "-" * 50 + "\n")

		for i, page in enumerate(ref_string, 1):

			prev_frames = frames.copy()
			victim = None
			change_type = "No Change"

			if page not in frames:
				page_faults += 1

				if len(frames) < frames_count:
					frames.append(page)
					change_type = "Inserted"
				else:
					if strategy == "LFU":
						# evict the page with the SMALLEST counter
						victim = min(frames, key=lambda p: counters.get(p, 0))
					else:  # MFU
						# evict the page with the LARGEST counter
						victim = max(frames, key=lambda p: counters.get(p, 0))

					victim_pos = frames.index(victim)
					frames[victim_pos] = page
					change_type = f"Replaced {victim} (count={counters.get(victim, 0)})"

				status = "FAULT"
			else:
				status = "HIT"

			# increment the reference counter for this page (hit or fault)
			counters[page] = counters.get(page, 0) + 1

			# build animation steps
			self.steps_queue.append((f"\nStep {i}", 300))
			self.steps_queue.append((f"Incoming Page: {page}", 300))
			self.steps_queue.append((f"Previous Frames: {prev_frames}", 300))

			if victim is not None:
				count_snapshot = {p: counters.get(p, 0) for p in prev_frames}
				self.steps_queue.append((f"Counts before eviction: {count_snapshot}", 300))
				self.steps_queue.append((f"Victim Chosen ({strategy}): {victim}", 300))

			if prev_frames != frames:
				self.steps_queue.append((f"Updated Frames: {frames} ⚡ ({change_type})", 400))
			else:
				self.steps_queue.append((f"Frames Unchanged: {frames}", 400))

			self.steps_queue.append((f"Page {page} count is now: {counters[page]}", 300))
			self.steps_queue.append((f"Status: {status}", 300))
			self.steps_queue.append(("-" * 50, 200))

		# start animation
		self.animate_steps(self.steps_queue)

		# final stats (delayed so UI doesn't feel frozen)
		total_delay = sum(delay for _, delay in self.steps_queue)
		self.root.after(total_delay, lambda: self.show_results(ref_string, page_faults, strategy))

	def animate_steps(self, steps, index=0):
		if index >= len(steps):
			return

		text, delay = steps[index]

		self.output.insert(tk.END, text + "\n")
		self.output.see(tk.END)

		self.root.after(delay, lambda: self.animate_steps(steps, index + 1))

	def show_results(self, ref_string, page_faults, strategy):
		hits = len(ref_string) - page_faults
		fault_ratio = page_faults / len(ref_string)
		hit_ratio = hits / len(ref_string)

		self.output.insert(tk.END, "\nFinal Results:\n")
		self.output.insert(tk.END, "-" * 50 + "\n")
		self.output.insert(tk.END, f"Strategy Used: {strategy}\n")
		self.output.insert(tk.END, f"Total References: {len(ref_string)}\n")
		self.output.insert(tk.END, f"Page Hits: {hits}\n")
		self.output.insert(tk.END, f"Page Faults: {page_faults}\n")
		self.output.insert(tk.END, f"Hit Ratio: {hit_ratio:.2f}\n")
		self.output.insert(tk.END, f"Fault Ratio: {fault_ratio:.2f}\n")
		self.output.see(tk.END)


if __name__ == "__main__":
	root = tk.Tk()
	app = CountingBasedSimulator(root)
	root.mainloop()