import tkinter as tk
from tkinter import messagebox


class MassStorageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mass Storage Management")
        self.root.geometry("950x700")

        self.setup_gui()

    def setup_gui(self):
        # Title
        tk.Label(
            self.root,
            text="Mass Storage Management Simulator",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Disk request input
        tk.Label(
            self.root,
            text="Enter Disk Requests (comma separated):"
        ).pack()

        self.request_entry = tk.Entry(self.root, width=50)
        self.request_entry.pack(pady=5)

        # Initial head position
        tk.Label(
            self.root,
            text="Enter Initial Head Position:"
        ).pack()

        self.head_entry = tk.Entry(self.root, width=20)
        self.head_entry.pack(pady=5)

        # Run button
        tk.Button(
            self.root,
            text="Run Simulation",
            command=self.run_simulation
        ).pack(pady=10)

        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=900,
            height=500,
            bg="white"
        )
        self.canvas.pack(pady=20)

    def run_simulation(self):
        try:
            requests = [
                int(x.strip())
                for x in self.request_entry.get().split(",")
            ]

            head = int(self.head_entry.get())

            self.show_graph(requests, head)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter valid numbers."
            )

    def show_graph(self, requests, head):
        self.canvas.delete("all")

        sequence = [head] + requests

        width = 850
        height = 450
        margin = 70
        legend_space = 180
        graph_width = width - legend_space

        max_track = max(sequence)
        min_track = min(sequence)

        if max_track == min_track:
            max_track += 1

        # Add padding so graph doesn't clip top/bottom
        padding = (max_track - min_track) * 0.15
        max_track += padding
        min_track -= padding

        # Shift graph right so initial head doesn't overlap Y-axis
        x_spacing = (graph_width - 2 * margin - 40) / (len(sequence) - 1)
        start_offset = 20

        # Grid lines
        for i in range(6):
            y = margin + i * ((height - 2 * margin) / 5)

            self.canvas.create_line(
                margin,
                y,
                graph_width - margin,
                y,
                fill="#d9d9d9",
                dash=(4, 2)
            )

            track_value = max_track - ((max_track - min_track) / 5) * i

            self.canvas.create_text(
                margin - 35,
                y,
                text=str(int(track_value)),
                font=("Arial", 9)
            )

        # X-axis labels
        for i in range(len(sequence)):
            x = margin + start_offset + i * x_spacing

            self.canvas.create_text(
                x,
                height - margin + 20,
                text=str(i),
                font=("Arial", 9)
            )

        # Axes
        self.canvas.create_line(
            margin,
            margin,
            margin,
            height - margin,
            width=2
        )

        self.canvas.create_line(
            margin,
            height - margin,
            graph_width - margin,
            height - margin,
            width=2
        )

        # Axis titles
        self.canvas.create_text(
            graph_width // 2,
            height - 20,
            text="Request Order",
            font=("Arial", 11, "bold")
        )

        self.canvas.create_text(
            25,
            height // 2,
            text="Track Number",
            angle=90,
            font=("Arial", 11, "bold")
        )

        points = []

        # Compute graph points
        for i, track in enumerate(sequence):
            x = margin + start_offset + i * x_spacing

            y = height - margin - (
                (track - min_track) / (max_track - min_track)
            ) * (height - 2 * margin)

            points.append((x, y))

        # Draw movement lines
        for i in range(len(points) - 1):
            self.canvas.create_line(
                points[i][0],
                points[i][1],
                points[i + 1][0],
                points[i + 1][1],
                fill="red",
                width=2,
                smooth=True
            )

        # Draw points
        for i, (x, y) in enumerate(points):
            color = "green" if i == 0 else "blue"

            self.canvas.create_oval(
                x - 7,
                y - 7,
                x + 7,
                y + 7,
                fill=color,
                outline="black"
            )

            self.canvas.create_text(
                x,
                y - 18,
                text=str(sequence[i]),
                font=("Arial", 9, "bold")
            )

        # Legend (outside graph)
        legend_x1 = graph_width + 10
        legend_y1 = 40
        legend_x2 = width - 20
        legend_y2 = 120

        self.canvas.create_rectangle(
            legend_x1,
            legend_y1,
            legend_x2,
            legend_y2,
            outline="black"
        )

        # Start position legend
        self.canvas.create_oval(
            legend_x1 + 15,
            legend_y1 + 15,
            legend_x1 + 30,
            legend_y1 + 30,
            fill="green"
        )

        self.canvas.create_text(
            legend_x1 + 90,
            legend_y1 + 22,
            text="Start Position"
        )

        # Disk request legend
        self.canvas.create_oval(
            legend_x1 + 15,
            legend_y1 + 50,
            legend_x1 + 30,
            legend_y1 + 65,
            fill="blue"
        )

        self.canvas.create_text(
            legend_x1 + 85,
            legend_y1 + 57,
            text="Disk Request"
        )


def main():
    root = tk.Tk()
    app = MassStorageGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()