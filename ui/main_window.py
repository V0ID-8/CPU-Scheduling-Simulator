# ui/main_window.py
# Main application window.
# Defines the top-level layout: left input panel, right chart panel,
# and bottom controls bar. Child widgets are imported from other modules.

import tkinter as tk
from tkinter import ttk

from ui import theme
from ui.process_table import ProcessTableWidget
from ui.controls_bar import ControlsBarWidget


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1050x680")
        self.root.configure(bg=theme.BG_PRIMARY)
        self.root.resizable(False, False)

        self._build_layout()

    def _build_layout(self):
        """
        Divides the window into three regions:
          - Left frame  : process input table
          - Right frame : Gantt chart display (populated in Step 4)
          - Bottom bar  : algorithm selector, quantum input, run button
        """

        # --- Top area: left + right panels side by side ---
        top_frame = tk.Frame(self.root, bg=theme.BG_PRIMARY)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))

        # Left panel — process input
        self.left_frame = tk.Frame(
            top_frame,
            bg=theme.BG_SECONDARY,
            width=370,
            relief=tk.FLAT,
            bd=0,
        )
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 8))
        self.left_frame.pack_propagate(False)

        # Right panel — Gantt chart placeholder
        self.right_frame = tk.Frame(
            top_frame,
            bg=theme.BG_SECONDARY,
            relief=tk.FLAT,
            bd=0,
        )
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Placeholder label in right panel (replaced in Step 4)
        placeholder = tk.Label(
            self.right_frame,
            text="Gantt chart will appear here after running the simulator.",
            bg=theme.BG_SECONDARY,
            fg=theme.TEXT_SECONDARY,
            font=theme.FONT_LABEL,
        )
        placeholder.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # --- Bottom controls bar ---
        self.controls_bar = ControlsBarWidget(self.root)
        self.controls_bar.frame.pack(
            fill=tk.X, padx=10, pady=10
        )

        # --- Attach process table to left panel ---
        self.process_table = ProcessTableWidget(self.left_frame)
        self.process_table.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run(self):
        self.root.mainloop()