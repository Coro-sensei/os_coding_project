import tkinter as tk
from tkinter import ttk, messagebox


class MassStorageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mass Storage Management")
        self.root.state("zoomed")

        self.setup_gui()

    def setup_gui(self):
        tk.Label(
            self.root,
            text="Mass Storage Management Simulator",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        tk.Label(
            self.root,
            text="Enter Disk Requests (comma separated):"
        ).pack()

        self.request_entry = tk.Entry(self.root, width=70)
        self.request_entry.pack(pady=5)

        tk.Label(
            self.root,
            text="Enter Initial Head Position:"
        ).pack()

        self.head_entry = tk.Entry(self.root, width=20)
        self.head_entry.pack(pady=5)

        tk.Label(
            self.root,
            text="Select Scheduling Algorithm:",
            font=("Arial", 12, "bold")
        ).pack()

        self.algorithm_var = tk.StringVar()

        self.algorithm_picker = ttk.Combobox(
            self.root,
            textvariable=self.algorithm_var,
            values=["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "CLOOK"],
            state="readonly"
        )
        self.algorithm_picker.pack(pady=5)
        self.algorithm_picker.current(0)

        tk.Label(
            self.root,
            text="Enter Disk Size (for SCAN / C-SCAN):"
        ).pack()

        self.disk_size_entry = tk.Entry(self.root, width=20)
        self.disk_size_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Run Simulation",
            command=self.run_simulation
        ).pack(pady=10)

        # graph area
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(fill="both", expand=True)

        self.h_scroll = tk.Scrollbar(
            canvas_frame,
            orient="horizontal"
        )
        self.h_scroll.pack(side="bottom", fill="x")

        self.v_scroll = tk.Scrollbar(
            canvas_frame,
            orient="vertical"
        )
        self.v_scroll.pack(side="right", fill="y")

        self.canvas = tk.Canvas(
            canvas_frame,
            bg="white",
            xscrollcommand=self.h_scroll.set,
            yscrollcommand=self.v_scroll.set
        )

        self.canvas.pack(fill="both", expand=True)

        self.h_scroll.config(command=self.canvas.xview)
        self.v_scroll.config(command=self.v_scroll.set)

    def run_simulation(self):
        try:
            requests = [
                int(x.strip())
                for x in self.request_entry.get().split(",")
                if x.strip()
            ]

            head = int(self.head_entry.get())

            disk_size_text = self.disk_size_entry.get().strip()
            disk_size = int(disk_size_text) if disk_size_text else None

            algorithm = self.algorithm_var.get()

            sequence = self.compute_sequence(
                requests,
                head,
                algorithm,
                disk_size
            )

            self.canvas.delete("all")
            self.canvas.xview_moveto(0)
            self.canvas.yview_moveto(0)

            self.show_graph(sequence)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter valid numeric values."
            )

    def compute_sequence(self, requests, head, algorithm, disk_size=None):
        if algorithm == "FCFS":
            return [head] + requests

        elif algorithm == "SSTF":
            return [head] + self.sstf_sequence(head, requests)

        elif algorithm == "SCAN":
            return [head] + self.scan_sequence(
                head,
                requests,
                disk_size
            )

        elif algorithm == "C-SCAN":
            return [head] + self.cscan_sequence(
                head,
                requests,
                disk_size
            )

        elif algorithm == "LOOK":
            return [head] + self.look_sequence(
                head,
                requests
            )

        elif algorithm == "CLOOK":
            return [head] + self.clook_sequence(
                head,
                requests
            )

        return [head] + requests

    # shortest seek time first
    def sstf_sequence(self, head, requests):
        remaining = list(requests)
        current = head
        sequence = []

        while remaining:
            nearest = min(
                remaining,
                key=lambda x: abs(x - current)
            )

            sequence.append(nearest)
            remaining.remove(nearest)
            current = nearest

        return sequence

    # scan
    def scan_sequence(self, head, requests, disk_size):
        if not requests:
            return []

        if disk_size is None:
            disk_size = max(requests) + 1

        requests = sorted(requests)

        left = [r for r in requests if r < head]
        right = [r for r in requests if r >= head]

        sequence = []

        sequence.extend(right)

        if right and right[-1] != disk_size - 1:
            sequence.append(disk_size - 1)

        sequence.extend(reversed(left))

        return sequence

    # circular scan
    def cscan_sequence(self, head, requests, disk_size):
        if not requests:
            return []

        if disk_size is None:
            disk_size = max(requests) + 1

        requests = sorted(requests)

        left = [r for r in requests if r < head]
        right = [r for r in requests if r >= head]

        sequence = []

        sequence.extend(right)

        if right and right[-1] != disk_size - 1:
            sequence.append(disk_size - 1)

        sequence.append(0)

        sequence.extend(left)

        return sequence

    # look
    def look_sequence(self, head, requests):
        if not requests:
            return []

        requests = sorted(requests)

        left = [r for r in requests if r < head]
        right = [r for r in requests if r >= head]

        sequence = []

        sequence.extend(right)
        sequence.extend(reversed(left))

        return sequence

    # circular look
    def clook_sequence(self, head, requests):
        if not requests:
            return []

        requests = sorted(requests)

        left = [r for r in requests if r < head]
        right = [r for r in requests if r >= head]

        sequence = []

        sequence.extend(right)
        sequence.extend(left)

        return sequence

    def show_graph(self, sequence):
        self.root.update_idletasks()

        max_track = max(sequence)
        min_track = min(sequence)

        canvas_width = max(
            self.canvas.winfo_width(),
            (max_track - min_track) * 6 + 500
        )

        canvas_height = max(
            self.canvas.winfo_height(),
            len(sequence) * 100
        )

        self.canvas.config(
            scrollregion=(0, 0, canvas_width, canvas_height)
        )

        left_margin = 150
        right_margin = 150
        top_margin = 80
        bottom_margin = 80

        graph_width = canvas_width - left_margin - right_margin
        graph_height = canvas_height - top_margin - bottom_margin

        if max_track == min_track:
            max_track += 1

        value_range = max_track - min_track
        padding = max(20, value_range * 0.15)

        scaled_max = max_track + padding
        scaled_min = min_track - padding

        y_spacing = graph_height / max(1, len(sequence) - 1)

        # grid
        for i in range(6):
            x = left_margin + i * (graph_width / 5)

            self.canvas.create_line(
                x,
                top_margin,
                x,
                top_margin + graph_height,
                fill="#cccccc",
                dash=(4, 2)
            )

            value = scaled_min + (
                (scaled_max - scaled_min) / 5
            ) * i

            self.canvas.create_text(
                x,
                top_margin + graph_height + 30,
                text=str(int(value))
            )

        points = []

        for i, track in enumerate(sequence):
            x = left_margin + (
                (track - scaled_min) /
                (scaled_max - scaled_min)
            ) * graph_width

            y = top_margin + i * y_spacing

            points.append((x, y))

            self.canvas.create_text(
                left_margin - 40,
                y,
                text=str(i)
            )

        # lines
        for i in range(len(points) - 1):
            self.canvas.create_line(
                points[i][0],
                points[i][1],
                points[i + 1][0],
                points[i + 1][1],
                fill="red",
                width=2
            )

        # points
        for i, (x, y) in enumerate(points):
            color = "green" if i == 0 else "blue"

            self.canvas.create_oval(
                x - 8,
                y - 8,
                x + 8,
                y + 8,
                fill=color
            )

            self.canvas.create_text(
                x + 30,
                y,
                text=str(sequence[i]),
                font=("Arial", 10, "bold")
            )


def main():
    root = tk.Tk()
    app = MassStorageGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()