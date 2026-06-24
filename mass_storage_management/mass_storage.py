import tkinter as tk
from tkinter import messagebox


class MassStorageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mass Storage Management")
        self.root.geometry("700x500")

        self.setup_gui()

    def setup_gui(self):
        # Title
        tk.Label(
            self.root,
            text="Mass Storage Management Simulator",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # Disk Request Input
        tk.Label(self.root, text="Enter Disk Requests (comma separated):").pack()
        self.request_entry = tk.Entry(self.root, width=40)
        self.request_entry.pack(pady=5)

        # Head Position Input
        tk.Label(self.root, text="Enter Initial Head Position:").pack()
        self.head_entry = tk.Entry(self.root, width=20)
        self.head_entry.pack(pady=5)

        # Run Button
        tk.Button(
            self.root,
            text="Run Simulation",
            command=self.run_simulation
        ).pack(pady=10)

        # Output Box
        self.output = tk.Text(self.root, width=80, height=15)
        self.output.pack(pady=10)

    def run_simulation(self):
        self.output.delete("1.0", tk.END)

        try:
            requests = [
                int(x.strip())
                for x in self.request_entry.get().split(",")
            ]
            head = int(self.head_entry.get())

            self.output.insert(tk.END, "Mass Storage Simulation Started\n")
            self.output.insert(tk.END, "-" * 40 + "\n")
            self.output.insert(tk.END, f"Requests: {requests}\n")
            self.output.insert(tk.END, f"Initial Head Position: {head}\n")

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter valid numbers."
            )



def main():
    root = tk.Tk()
    app = MassStorageGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()