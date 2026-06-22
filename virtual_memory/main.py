import tkinter as tk
from tkinter import messagebox

from fifo_pr import FIFOSimulator
from LRU_pr import LRUSimulator
from LRU_approx_pr import LRUApproxSimulator
from optimal_pr import OptimalSimulator
from countingbased_pr import CountingBasedSimulator

SIMULATIONS = [
    ("FIFO Page Replacement", FIFOSimulator),
    ("LRU Page Replacement", LRUSimulator),
    ("LRU Approximation (Second-Chance)", LRUApproxSimulator),
    ("Optimal Page Replacement", OptimalSimulator),
    ("Counting-Based (LFU / MFU)", CountingBasedSimulator),
]

SIMULATION_DESCRIPTIONS = {
    "FIFO Page Replacement": "First-In First-Out replacement method.",
    "LRU Page Replacement": "Least Recently Used replacement method.",
    "LRU Approximation (Second-Chance)": "Second-Chance clock algorithm approximation of LRU.",
    "Optimal Page Replacement": "Optimal replacement using future reference information.",
    "Counting-Based (LFU / MFU)": "Counting-based replacement using LFU or MFU strategy.",
}


class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Memory Page Replacement Simulator")
        self.root.geometry("620x380")
        self.root.resizable(False, False)

        title = tk.Label(root, text="Page Replacement Simulator Menu",
                         font=("Arial", 20, "bold"))
        title.pack(pady=(20, 10))

        description = tk.Label(root,
                               text="Select a simulation and click Run to open the simulator window.",
                               font=("Arial", 12), wraplength=560, justify="center")
        description.pack(pady=(0, 15))

        self.selected_simulation = tk.StringVar(value=SIMULATIONS[0][0])

        radio_frame = tk.Frame(root)
        radio_frame.pack(pady=10)

        for name, _ in SIMULATIONS:
            tk.Radiobutton(radio_frame,
                           text=name,
                           variable=self.selected_simulation,
                           value=name,
                           anchor="w",
                           justify="left",
                           width=35,
                           padx=4).pack(anchor="w", pady=2)

        self.detail_label = tk.Label(root,
                                     text=SIMULATION_DESCRIPTIONS[self.selected_simulation.get()],
                                     font=("Arial", 11),
                                     wraplength=560,
                                     justify="center")
        self.detail_label.pack(pady=(10, 0))

        self.selected_simulation.trace_add("write", self.update_description)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Run Selected Simulation", command=self.open_simulation,
                  bg="#4CAF50", fg="white", padx=12, pady=8).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Quit", command=self.root.quit,
                  bg="#f44336", fg="white", padx=12, pady=8).grid(row=0, column=1, padx=5)

        footer = tk.Label(root,
                          text="Built for FIFO, LRU, LRU Approximation, Optimal, and Counting-Based simulations.",
                          font=("Arial", 9), wraplength=560)
        footer.pack(side="bottom", pady=10)

    def update_description(self, *args):
        name = self.selected_simulation.get()
        self.detail_label.config(text=SIMULATION_DESCRIPTIONS.get(name, ""))

    def open_simulation(self):
        selection = self.selected_simulation.get()
        simulator_class = next((cls for name, cls in SIMULATIONS if name == selection), None)

        if simulator_class is None:
            messagebox.showerror("Selection Error", "Please choose a valid simulation.")
            return

        simulator_window = tk.Toplevel(self.root)
        simulator_window.transient(self.root)
        simulator_window.grab_set()

        simulator = simulator_class(simulator_window)
        simulator_window.protocol("WM_DELETE_WINDOW", lambda: self.close_simulator(simulator_window))

    def close_simulator(self, window):
        window.grab_release()
        window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()
