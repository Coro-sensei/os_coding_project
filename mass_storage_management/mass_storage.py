import tkinter as tk
from tkinter import ttk, messagebox

def calc_movement(path):
    return sum(abs(path[i] - path[i+1]) for i in range(len(path) - 1))

def calculate_fcfs(queue, head):
    path = [head] + queue
    return path, calc_movement(path)

def calculate_sstf(queue, head):
    path = [head]
    unvisited = queue.copy()
    current = head
    while unvisited:
        closest = min(unvisited, key=lambda x: abs(x - current))
        path.append(closest)
        unvisited.remove(closest)
        current = closest
    return path, calc_movement(path)

def calculate_scan(queue, head, max_track=199):
    path = [head]
    left = sorted([x for x in queue if x < head])
    right = sorted([x for x in queue if x >= head])

    path.extend(right)
    if right and right[-1] != max_track:
        path.append(max_track)
    path.extend(reversed(left))
    return path, calc_movement(path)

def calculate_cscan(queue, head, max_track=199):
    path = [head]
    left = sorted([x for x in queue if x < head])
    right = sorted([x for x in queue if x >= head])

    path.extend(right)
    path.append(max_track)
    path.append(0)
    path.extend(left)
    return path, calc_movement(path)

def calculate_look(queue, head):
    path = [head]
    left = sorted([x for x in queue if x < head])
    right = sorted([x for x in queue if x >= head])

    path.extend(right)
    path.extend(reversed(left))
    return path, calc_movement(path)

def calculate_clook(queue, head):
    path = [head]
    left = sorted([x for x in queue if x < head])
    right = sorted([x for x in queue if x >= head])

    path.extend(right)
    path.extend(left)
    return path, calc_movement(path)

def draw_graph(path):
    canvas.delete("all")
    if not path: return

    c_width, c_height = 550, 350
    pad_x, pad_y = 20, 20

    max_track = max(max(path), 199)

    points = []
    for index, track in enumerate(path):
        x = pad_x + (track / max_track) * (c_width - 2 * pad_x)
        y = pad_y + (index / max(1, len(path) - 1)) * (c_height - 2 * pad_y)
        points.append((x, y)

        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")
        canvas.create_text(x, y - 10, text=str(track), font=("Arial", 8))

        for i in range(len(points) - 1):
            canvas.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], fill="blue", width=2)

def run_visualizer():
    try:
        queue = [int(x.strip()) for x in entry_queue.get().split(",")]
        head = int(entry_head.get())
        algo = combo_algo.get()

        if algo == "FCFS":
            path, total = calculate_fcfs(queue, head)
        elif algo == "SSTF":
            path, total = calculate_sstf(queue, head)
        elif algo == "SCAN":
            path, total = calculate_scan(queue, head)
        elif algo == "C-SCAN":
            path, total = calculate_cscan(queue, head)
        elif algo == "LOOK":
            path, total = calculate_look(queue, head)
        elif algo == "C-LOOK":
            path, total = calculate_clook(queue, head)

        lbl_result.config(text=f"Algorithm: {algo} | Total Movement: {total}\nPath: {' -> '.join(map(str, path))}")
        draw_graph(path)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

root = tk.Tk()
root.title("Mass Storage Management - Visualizer")
root.geometry("650x650")

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Queue (comma separated):").grid(row=0, column=0, padx=5, pady=5)
entry_queue = tk.Entry(frame_inputs, width=40)
entry_queue.grid(row=0, column=1, padx=5, pady=5)
entry_queue.insert(0, "98, 183, 37, 122, 14, 124, 65, 67")

tk.Label(frame_inputs, text="Initial Head:").grid(row=1, column=0, padx=5, pady=5)
entry_head = tk.Entry(frame_inputs, width=10)
entry_head.grid(row=1, column=1, sticky="w", padx=5, pady=5)
entry_head.insert(0, "53")

tk.Label(frame_inputs, text="Algorithm: ").grid(row=2, column=0, padx=5, pady=5)
combo_algo = ttk.Combobox(frame_inputes, values=["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"], state="readonly")
combo_algo.grid(row=2, column=1, sticky="w", padx=5, pady=5)
combo_algo.current(0)