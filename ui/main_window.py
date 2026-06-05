# ui/main_window.py
# Main application window.

import tkinter as tk


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("900x650")

    def run(self):
        self.root.mainloop()