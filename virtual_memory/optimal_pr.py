import tkinter as tk
from tkinter import messagebox

MAX_REFERENCES = 20
MAX_FRAMES = 10


class OptimalSimulator:
	def __init__(self, root):
		self.root = root
		self.root.title("Optimal Page Replacement Simulator")
		self.root.geometry("700x600")

		# Title
		tk.Label(root, text="Optimal Page Replacement Simulator",
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
		tk.Button(root, text="Run Simulation", command=self.run_optimal,
				  bg="blue", fg="white").pack(pady=10)

		# Output box
		self.output = tk.Text(root, height=20, width=80)
		self.output.pack(pady=10)

	def run_optimal(self):
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

		frames = []
		page_faults = 0
		self.steps_queue = []

		self.output.insert(tk.END, "Optimal Page Replacement Simulation Steps:\n")
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
					# Look ahead: find the page in frames whose NEXT use is
					# furthest away (or never used again -> evict that one).
					future = ref_string[i:]  # references after current index
					farthest_index = -1
					victim = None

					for f_page in frames:
						if f_page in future:
							next_use = future.index(f_page)
						else:
							next_use = float("inf")  # never used again

						if next_use > farthest_index:
							farthest_index = next_use
							victim = f_page

					victim_pos = frames.index(victim)
					frames[victim_pos] = page
					change_type = f"Replaced {victim} (next use farthest/never)"

				status = "FAULT"
			else:
				status = "HIT"

			# build animation steps
			self.steps_queue.append((f"\nStep {i}", 300))
			self.steps_queue.append((f"Incoming Page: {page}", 300))
			self.steps_queue.append((f"Previous Frames: {prev_frames}", 300))

			if victim is not None:
				self.steps_queue.append((f"Lookahead: {ref_string[i:]}", 300))
				self.steps_queue.append((f"Victim Chosen: {victim}", 300))

			if prev_frames != frames:
				self.steps_queue.append((f"Updated Frames: {frames}  ({change_type})", 400))
			else:
				self.steps_queue.append((f"Frames Unchanged: {frames}", 400))

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
	app = OptimalSimulator(root)
	root.mainloop()
