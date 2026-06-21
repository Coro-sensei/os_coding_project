import tkinter as tk
from tkinter import messagebox

MAX_REFERENCES = 20
MAX_FRAMES = 10


class FIFOSimulator:
	def __init__(self, root):
		self.root = root
		self.root.title("FIFO Page Replacement Simulator")
		self.root.geometry("700x600")

		# Title
		tk.Label(root, text="FIFO Page Replacement Simulator",
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
		tk.Button(root, text="Run Simulation", command=self.run_fifo,
				  bg="green", fg="white").pack(pady=10)

		# Output box
		self.output = tk.Text(root, height=20, width=80)
		self.output.pack(pady=10)

	def run_fifo(self):
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

		self.output.insert(tk.END, "FIFO Simulation Steps:\n")
		self.output.insert(tk.END, "-" * 50 + "\n")

		# ✅ FIXED LOOP (THIS WAS BROKEN IN YOUR CODE)
		for i, page in enumerate(ref_string, 1):

			prev_frames = frames.copy()

			if page not in frames:
				page_faults += 1

				if len(frames) < frames_count:
					frames.append(page)
				else:
					frames.pop(0)
					frames.append(page)

				status = "FAULT"
				change_type = "Inserted/Replaced"
			else:
				status = "HIT"
				change_type = "No Change"

			# build animation steps properly
			self.steps_queue.append((f"\nStep {i}", 300))
			self.steps_queue.append((f"Incoming Page: {page}", 300))
			self.steps_queue.append((f"Previous Frames: {prev_frames}", 300))

			if prev_frames != frames:
				self.steps_queue.append((f"Updated Frames: {frames}  ({change_type})", 400))
			else:
				self.steps_queue.append((f"Frames Unchanged: {frames}", 400))

			self.steps_queue.append((f"Status: {status}", 300))
			self.steps_queue.append(("-" * 50, 200))

		# start animation
		self.animate_steps(self.steps_queue)

		# final stats (delayed so UI doesn't feel frozen)
		self.root.after(len(self.steps_queue) * 400, lambda: self.show_results(ref_string, page_faults))

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


if __name__ == "__main__":
	root = tk.Tk()
	app = FIFOSimulator(root)
	root.mainloop()