import tkinter as tk
from tkinter import ttk, messagebox


# Process class
class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.reset()

    def reset(self):
        self.remaining = self.burst
        self.start = None
        self.finish = None
        self.waiting = 0
        self.turnaround = 0
        self.response = -1


# Scheduling functions
class Scheduler:
    def reset_processes(self, processes):
        for p in processes:
            p.reset()

    # First Come First Serve
    def fcfs(self, processes):
        self.reset_processes(processes)
        time = 0
        timeline = []

        for p in sorted(processes, key=lambda x: x.arrival):
            if time < p.arrival:
                time = p.arrival

            p.start = time
            p.response = time - p.arrival
            time += p.burst
            p.finish = time
            p.turnaround = p.finish - p.arrival
            p.waiting = p.turnaround - p.burst

            timeline.append((p.pid, p.start, p.finish))

        return timeline

    # Shortest Job First
    def sjf(self, processes):
        self.reset_processes(processes)
        time = 0
        completed = []
        timeline = []

        while len(completed) < len(processes):
            ready = [p for p in processes if p.arrival <= time and p not in completed]

            if not ready:
                time += 1
                continue

            current = min(ready, key=lambda x: x.burst)

            current.start = time
            current.response = time - current.arrival
            time += current.burst
            current.finish = time
            current.turnaround = current.finish - current.arrival
            current.waiting = current.turnaround - current.burst

            completed.append(current)
            timeline.append((current.pid, current.start, current.finish))

        return timeline

    # Shortest Remaining Time First
    def srtf(self, processes):
        self.reset_processes(processes)
        time = 0
        completed = 0
        timeline = []

        while completed < len(processes):
            ready = [p for p in processes if p.arrival <= time and p.remaining > 0]

            if not ready:
                time += 1
                continue

            current = min(ready, key=lambda x: x.remaining)

            if current.response == -1:
                current.response = time - current.arrival

            start = time
            current.remaining -= 1
            time += 1

            if current.remaining == 0:
                current.finish = time
                current.turnaround = time - current.arrival
                current.waiting = current.turnaround - current.burst
                completed += 1

            timeline.append((current.pid, start, time))

        return timeline

    # Priority Non-Preemptive
    def priority_np(self, processes):
        self.reset_processes(processes)
        time = 0
        completed = []
        timeline = []

        while len(completed) < len(processes):
            ready = [p for p in processes if p.arrival <= time and p not in completed]

            if not ready:
                time += 1
                continue

            current = min(ready, key=lambda x: x.priority)

            current.start = time
            current.response = time - current.arrival
            time += current.burst
            current.finish = time
            current.turnaround = current.finish - current.arrival
            current.waiting = current.turnaround - current.burst

            completed.append(current)
            timeline.append((current.pid, current.start, current.finish))

        return timeline

    # Priority Preemptive
    def priority_p(self, processes):
        self.reset_processes(processes)
        time = 0
        completed = 0
        timeline = []

        while completed < len(processes):
            ready = [p for p in processes if p.arrival <= time and p.remaining > 0]

            if not ready:
                time += 1
                continue

            current = min(ready, key=lambda x: x.priority)

            if current.response == -1:
                current.response = time - current.arrival

            start = time
            current.remaining -= 1
            time += 1

            if current.remaining == 0:
                current.finish = time
                current.turnaround = time - current.arrival
                current.waiting = current.turnaround - current.burst
                completed += 1

            timeline.append((current.pid, start, time))

        return timeline

    # Round Robin
    def round_robin(self, processes, quantum):
        self.reset_processes(processes)

        time = 0
        queue = []
        timeline = []
        added = set()

        while True:
            for p in processes:
                if p.arrival <= time and p not in added and p.remaining > 0:
                    queue.append(p)
                    added.add(p)

            if not queue:
                if all(p.remaining == 0 for p in processes):
                    break
                time += 1
                continue

            current = queue.pop(0)

            if current.response == -1:
                current.response = time - current.arrival

            start = time
            execute = min(quantum, current.remaining)

            current.remaining -= execute
            time += execute

            timeline.append((current.pid, start, time))

            for p in processes:
                if p.arrival <= time and p.remaining > 0 and p not in queue and p != current:
                    queue.append(p)

            if current.remaining > 0:
                queue.append(current)
            else:
                current.finish = time
                current.turnaround = time - current.arrival
                current.waiting = current.turnaround - current.burst

        return timeline


# Main app
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.state("zoomed")

        self.scheduler = Scheduler()
        self.processes = []

        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # shows process added
        self.status_label = tk.Label(
            self.root,
            text="",
            fg="green",
            font=("Arial", 11, "bold")
        )
        self.status_label.pack()

        tk.Label(frame, text="Arrival").grid(row=0, column=0)
        tk.Label(frame, text="Burst").grid(row=0, column=1)
        tk.Label(frame, text="Priority").grid(row=0, column=2)

        self.arrival_entry = tk.Entry(frame)
        self.burst_entry = tk.Entry(frame)
        self.priority_entry = tk.Entry(frame)

        self.arrival_entry.grid(row=1, column=0)
        self.burst_entry.grid(row=1, column=1)
        self.priority_entry.grid(row=1, column=2)

        tk.Button(frame, text="Add Process", command=self.add_process).grid(row=1, column=3)
        tk.Button(frame, text="Clear Processes", command=self.clear_processes).grid(row=1, column=4)

        self.algorithm = ttk.Combobox(
            self.root,
            values=["FCFS", "SJF", "SRTF", "Priority NP", "Priority P", "Round Robin"]
        )
        self.algorithm.pack()
        self.algorithm.current(0)

        tk.Label(self.root, text="Quantum").pack()
        self.quantum_entry = tk.Entry(self.root)
        self.quantum_entry.pack()

        tk.Button(self.root, text="Run Simulation", command=self.run).pack(pady=10)

        self.tree = ttk.Treeview(
            self.root,
            columns=("PID", "AT", "BT", "WT", "TAT"),
            show="headings"
        )
        self.tree.pack(fill="x")

        for col in ("PID", "AT", "BT", "WT", "TAT"):
            self.tree.heading(col, text=col)

        # gantt chart area
        gantt_frame = tk.Frame(self.root)
        gantt_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(gantt_frame, bg="white", height=250)
        self.scroll_x = tk.Scrollbar(gantt_frame, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(xscrollcommand=self.scroll_x.set)

        self.canvas.pack(fill="both", expand=True)
        self.scroll_x.pack(fill="x")

    def add_process(self):
        try:
            pid = f"P{len(self.processes)+1}"
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            priority = int(self.priority_entry.get()) if self.priority_entry.get() else 0

            self.processes.append(Process(pid, arrival, burst, priority))

            self.status_label.config(text=f"{pid} added")
            self.root.after(3000, lambda: self.status_label.config(text=""))

            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers.")

    def clear_processes(self):
        self.processes.clear()
        self.tree.delete(*self.tree.get_children())
        self.canvas.delete("all")

    def run(self):
        if not self.processes:
            messagebox.showerror("Error", "No processes added.")
            return

        algo = self.algorithm.get()

        if algo == "FCFS":
            timeline = self.scheduler.fcfs(self.processes)
        elif algo == "SJF":
            timeline = self.scheduler.sjf(self.processes)
        elif algo == "SRTF":
            timeline = self.scheduler.srtf(self.processes)
        elif algo == "Priority NP":
            timeline = self.scheduler.priority_np(self.processes)
        elif algo == "Priority P":
            timeline = self.scheduler.priority_p(self.processes)
        else:
            q = int(self.quantum_entry.get())
            timeline = self.scheduler.round_robin(self.processes, q)

        self.show_results()
        self.draw_gantt(timeline)

    def show_results(self):
        self.tree.delete(*self.tree.get_children())

        for p in self.processes:
            self.tree.insert("", "end", values=(p.pid, p.arrival, p.burst, p.waiting, p.turnaround))

    # combines same process blocks
    def compress_timeline(self, timeline):
        if not timeline:
            return []

        compressed = [timeline[0]]

        for pid, start, end in timeline[1:]:
            last_pid, last_start, last_end = compressed[-1]

            if pid == last_pid and start == last_end:
                compressed[-1] = (last_pid, last_start, end)
            else:
                compressed.append((pid, start, end))

        return compressed

    def draw_gantt(self, timeline):
        self.canvas.delete("all")
        timeline = self.compress_timeline(timeline)

        if not timeline:
            return

        self.root.update_idletasks()

        total_time = timeline[-1][2]
        visible_width = self.root.winfo_width() - 80
        scale = max(25, min(80, (visible_width - 40) / total_time))

        x = 20
        y1 = 60
        y2 = 120

        for pid, start, end in timeline:
            width = (end - start) * scale

            self.canvas.create_rectangle(x, y1, x + width, y2)
            self.canvas.create_text(x + width / 2, 90, text=pid)
            self.canvas.create_text(x, 140, text=str(start))

            x += width

        self.canvas.create_text(x, 140, text=str(total_time))

        self.canvas.config(
            width=visible_width,
            scrollregion=(0, 0, max(visible_width, x + 20), 200)
        )

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()