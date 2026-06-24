import tkinter as tk
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

        tk.Label(
            root,
            text="Virtual Memory Simulator",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Button(root, text="FIFO", width=30, command=self.run_fifo).pack(pady=10)
        tk.Button(root, text="LRU", width=30, command=self.run_lru).pack(pady=10)
        tk.Button(root, text="LRU Approximation", width=30, command=self.run_lru_approx).pack(pady=10)
        tk.Button(root, text="Optimal", width=30, command=self.run_optimal).pack(pady=10)
        tk.Button(root, text="Counting Based", width=30, command=self.run_counting).pack(pady=10)

    def run_fifo(self):
        win = tk.Toplevel(self.root)
        fifo_pr.FIFOSimulator(win)

    def run_lru(self):
        win = tk.Toplevel(self.root)
        LRU_pr.LRUSimulator(win)

    def run_lru_approx(self):
        win = tk.Toplevel(self.root)
        LRU_approx_pr.LRUApproxSimulator(win)

    def run_optimal(self):
        win = tk.Toplevel(self.root)
        optimal_pr.OptimalSimulator(win)

    def run_counting(self):
        win = tk.Toplevel(self.root)
        countingbased_pr.CountingBasedSimulator(win)


def main():
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()