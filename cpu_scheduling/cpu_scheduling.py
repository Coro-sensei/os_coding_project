import tkinter as tk
from tkinter import ttk, messagebox


# ---------------- PROCESS CLASS ----------------
class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst

        self.start = None
        self.finish = None
        self.waiting = 0
        self.turnaround = 0
        self.response = -1


# ---------------- CPU SCHEDULER ----------------
class Scheduler:

    # FCFS
    def fcfs(self, processes):
        time = 0
        timeline = []

        processes.sort(key=lambda x: x.arrival)

        for p in processes:
            if time < p.arrival:
                time = p.arrival

            p.start = time
            p.response = p.start - p.arrival

            time += p.burst
            p.finish = time

            p.turnaround = p.finish - p.arrival
            p.waiting = p.turnaround - p.burst

            timeline.append((p.pid, p.start, p.finish))

        return timeline

    # Non-preemptive SJF
    def sjf(self, processes):
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

    # Preemptive SJF (SRTF)
    def srtf(self, processes):
        time = 0
        complete = 0
        timeline = []

        while complete < len(processes):
            ready = [p for p in processes if p.arrival <= time and p.remaining > 0]

            if not ready:
                time += 1
                continue

            current = min(ready, key=lambda x: x.remaining)

            if current.response == -1:
                current.response = time - current.arrival
                current.start = time

            start = time
            current.remaining -= 1
            time += 1

            if current.remaining == 0:
                current.finish = time
                current.turnaround = current.finish - current.arrival
                current.waiting = current.turnaround - current.burst
                complete += 1

            timeline.append((current.pid, start, time))

        return timeline

    # Priority Non-preemptive
    def priority_np(self, processes):
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
        time = 0
        complete = 0
        timeline = []

        while complete < len(processes):
            ready = [p for p in processes if p.arrival <= time and p.remaining > 0]

            if not ready:
                time += 1
                continue

            current = min(ready, key=lambda x: x.priority)

            if current.response == -1:
                current.response = time - current.arrival
                current.start = time

            start = time
            current.remaining -= 1
            time += 1

            if current.remaining == 0:
                current.finish = time
                current.turnaround = current.finish - current.arrival
                current.waiting = current.turnaround - current.burst
                complete += 1

            timeline.append((current.pid, start, time))

        return timeline

    # Round Robin
    def round_robin(self, processes, quantum):
        time = 0
        queue = []
        timeline = []

        processes.sort(key=lambda x: x.arrival)
        queue.append(processes[0])

        while queue:
            current = queue.pop(0)

            if current.response == -1:
                current.response = time - current.arrival

            start = time
            execute = min(quantum, current.remaining)

            current.remaining -= execute
            time += execute

            timeline.append((current.pid, start, time))

            for p in processes:
                if p.arrival <= time and p not in queue and p.remaining > 0 and p != current:
                    queue.append(p)

            if current.remaining > 0:
                queue.append(current)
            else:
                current.finish = time
                current.turnaround = current.finish - current.arrival
                current.waiting = current.turnaround - current.burst

        return timeline


# ---------------- GUI ----------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.scheduler = Scheduler()
        self.processes = []

        # Input frame
        frame = tk.Frame(root)
        frame.pack(pady=10)

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

        # Algorithm selector
        self.algorithm = ttk.Combobox(root, values=[
            "FCFS",
            "SJF",
            "SRTF",
            "Priority NP",
            "Priority P",
            "Round Robin"
        ])
        self.algorithm.pack()

        self.quantum_entry = tk.Entry(root)
        self.quantum_entry.pack()
        self.quantum_entry.insert(0, "Quantum (RR only)")

        tk.Button(root, text="Run Simulation", command=self.run).pack(pady=10)

        # Table
        self.tree = ttk.Treeview(root, columns=("PID", "AT", "BT", "WT", "TAT"))
        self.tree.pack()

        for col in ("PID", "AT", "BT", "WT", "TAT"):
            self.tree.heading(col, text=col)

        # Gantt Chart Canvas
        self.canvas = tk.Canvas(root, width=800, height=200, bg="white")
        self.canvas.pack()

    def add_process(self):
        pid = f"P{len(self.processes)+1}"
        arrival = int(self.arrival_entry.get())
        burst = int(self.burst_entry.get())
        priority = int(self.priority_entry.get())

        self.processes.append(Process(pid, arrival, burst, priority))

        messagebox.showinfo("Success", f"{pid} added!")

    def run(self):
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
        elif algo == "Round Robin":
            q = int(self.quantum_entry.get())
            timeline = self.scheduler.round_robin(self.processes, q)

        self.show_results()
        self.draw_gantt(timeline)

    def show_results(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in self.processes:
            self.tree.insert("", "end", values=(
                p.pid, p.arrival, p.burst,
                p.waiting, p.turnaround
            ))

    def draw_gantt(self, timeline):
        self.canvas.delete("all")

        x = 20
        for pid, start, end in timeline:
            width = (end - start) * 40

            self.canvas.create_rectangle(x, 50, x + width, 100)
            self.canvas.create_text(x + width / 2, 75, text=pid)

            self.canvas.create_text(x, 110, text=str(start))
            x += width

        self.canvas.create_text(x, 110, text=str(timeline[-1][2]))


# ---------------- MAIN ----------------
root = tk.Tk()
app = App(root)
root.mainloop()
