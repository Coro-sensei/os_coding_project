import tkinter as tk

# Import page replacement modules
import fifo_pr
import LRU_pr
import LRU_approx_pr
import optimal_pr
import countingbased_pr


class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Memory Simulator")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        self.setup_gui()

    def setup_gui(self):
        # Title
        tk.Label(
            self.root,
            text="Virtual Memory Simulator",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="Choose a Page Replacement Algorithm",
            font=("Arial", 12)
        ).pack(pady=10)

        # Buttons 
        tk.Button(
            self.root,
            text="FIFO",
            width=30,
            height=2,
            command=self.run_fifo
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="LRU",
            width=30,
            height=2,
            command=self.run_lru
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="LRU Approximation",
            width=30,
            height=2,
            command=self.run_lru_approx
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Optimal",
            width=30,
            height=2,
            command=self.run_optimal
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Counting Based (LFU/MFU)",
            width=30,
            height=2,
            command=self.run_counting
        ).pack(pady=10)

    # Open each simulator in a new window
    def run_fifo(self):
        new_window = tk.Toplevel(self.root)
        fifo_pr.FIFOSimulator(new_window)

    def run_lru(self):
        new_window = tk.Toplevel(self.root)
        LRU_pr.LRUSimulator(new_window)

    def run_lru_approx(self):
        new_window = tk.Toplevel(self.root)
        LRU_approx_pr.LRUApproxSimulator(new_window)

    def run_optimal(self):
        new_window = tk.Toplevel(self.root)
        optimal_pr.OptimalSimulator(new_window)

    def run_counting(self):
        new_window = tk.Toplevel(self.root)
        countingbased_pr.CountingBasedSimulator(new_window)


# Main launcher
def main():
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()