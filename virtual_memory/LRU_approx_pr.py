import tkinter as tk
from tkinter import messagebox

MAX_REFERENCES = 20
MAX_FRAMES = 10


class LRUApproxSimulator:
	"""
	LRU Approximation using the Second-Chance (Clock) Algorithm.

	Each frame holds a page + a reference bit (R).
	- On a HIT: set R = 1 for that page (mark it "recently used").
	- On a FAULT with free space: insert page, R = 1, advance pointer.
	- On a FAULT with frames full: a circular "clock hand" pointer scans
	frames. If R == 1, give it a "second chance" -> set R = 0 and move
	the hand forward (don't evict yet). If R == 0, evict that page,
	insert the new one (R = 1), and move the hand past it.
	"""

	def __init__(self, root):
		self.root = root
		self.root.title("LRU Approximation (Second-Chance) Simulator")
		self.root.geometry("700x600")

		# Title
		tk.Label(root, text="LRU Approximation (Second-Chance / Clock)",
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

		# Run button
		tk.Button(root, text="Run Simulation", command=self.run_lru_approx,
				bg="darkorange", fg="white").pack(pady=10)

		# Output box
		self.output = tk.Text(root, height=20, width=80)
		self.output.pack(pady=10)

	def run_lru_approx(self):
		self.output.delete("1.0", tk.END)

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

		# frames[slot] = page number or None (empty)
		frames = [None] * frames_count
		# ref_bits[slot] = 0 or 1
		ref_bits = [0] * frames_count
		pointer = 0  # the "clock hand"
		page_faults = 0
		self.steps_queue = []

		self.output.insert(tk.END, "LRU Approximation (Second-Chance) Simulation Steps:\n")
		self.output.insert(tk.END, "-" * 50 + "\n")

		for i, page in enumerate(ref_string, 1):

			prev_frames = frames.copy()
			prev_bits = ref_bits.copy()
			scan_log = []
			change_type = "No Change"

			if page in frames:
				# HIT: just refresh the reference bit
				slot = frames.index(page)
				ref_bits[slot] = 1
				status = "HIT"
				change_type = f"Set R-bit=1 for page {page}"
			else:
				page_faults += 1
				status = "FAULT"

				if None in frames:
					# free slot available, fill it (no clock scanning needed yet)
					slot = frames.index(None)
					frames[slot] = page
					ref_bits[slot] = 1
					pointer = (slot + 1) % frames_count
					change_type = f"Inserted into empty slot {slot}"
				else:
					# Clock algorithm: scan from pointer for a victim (R == 0)
					while True:
						scan_log.append(f"slot{pointer}=page{frames[pointer]}(R={ref_bits[pointer]})")
						if ref_bits[pointer] == 0:
							victim = frames[pointer]
							frames[pointer] = page
							ref_bits[pointer] = 1
							change_type = f"Replaced page {victim} at slot {pointer}"
							pointer = (pointer + 1) % frames_count
							break
						else:
							ref_bits[pointer] = 0  # give second chance
							pointer = (pointer + 1) % frames_count

			# build animation steps
			self.steps_queue.append((f"\nStep {i}", 300))
			self.steps_queue.append((f"Incoming Page: {page}", 300))
			self.steps_queue.append((f"Previous Frames: {prev_frames}", 300))
			self.steps_queue.append((f"Previous R-bits:  {prev_bits}", 300))

			if scan_log:
				self.steps_queue.append((f"Clock Scan: {' -> '.join(scan_log)}", 400))

			self.steps_queue.append((f"Updated Frames: {frames}  R-bits: {ref_bits} ⚡ ({change_type})", 400))
			self.steps_queue.append((f"Status: {status}", 300))
			self.steps_queue.append(("-" * 50, 200))

		# start animation
		self.animate_steps(self.steps_queue)

		# final stats (delayed so UI doesn't feel frozen)
		total_delay = sum(delay for _, delay in self.steps_queue)
		self.root.after(total_delay, lambda: self.show_results(ref_string, page_faults))

	def animate_steps(self, steps, index=0):
		if index >= len(steps):
			return

		text, delay = steps[index]

		self.output.insert(tk.END, text + "\n")
		self.output.see(tk.END)

		self.root.after(delay, lambda: self.animate_steps(steps, index + 1))

	def show_results(self, ref_string, page_faults):
		hits = len(ref_string) - page_faults
		fault_ratio = page_faults / len(ref_string)
		hit_ratio = hits / len(ref_string)

		self.output.insert(tk.END, "\nFinal Results:\n")
		self.output.insert(tk.END, "-" * 50 + "\n")
		self.output.insert(tk.END, f"Total References: {len(ref_string)}\n")
		self.output.insert(tk.END, f"Page Hits: {hits}\n")
		self.output.insert(tk.END, f"Page Faults: {page_faults}\n")
		self.output.insert(tk.END, f"Hit Ratio: {hit_ratio:.2f}\n")
		self.output.insert(tk.END, f"Fault Ratio: {fault_ratio:.2f}\n")
		self.output.see(tk.END)


if __name__ == "__main__":
	root = tk.Tk()
	app = LRUApproxSimulator(root)
	root.mainloop()