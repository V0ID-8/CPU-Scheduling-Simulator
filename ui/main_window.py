# ui/main_window.py
# Main application window.
# Owns the layout and coordinates between the process table,
# controls bar, Gantt chart, and results table.
# All algorithm calls are dispatched through this file.

import tkinter as tk
from tkinter import messagebox

from ui import theme
from ui.process_table import ProcessTableWidget
from ui.controls_bar import ControlsBarWidget
from ui.gantt_chart import GanttChartWidget
from ui.results_table import ResultsTableWidget
from algorithms.scheduler import run_scheduler


# Maps the full dropdown label to the short key the router expects
ALGORITHM_KEY_MAP = {
    "First Come First Served (FCFS)": "FCFS",
    "Shortest Job First (SJF)": "SJF",
    "Round Robin (RR)": "RR",
    "Priority Scheduling": "PRIORITY",
}


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1100x700")
        self.root.configure(bg=theme.BG_PRIMARY)
        self.root.resizable(False, False)

        self._build_layout()
        self._wire_controls()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build_layout(self):
        """
        Window is divided into:
          - top_frame : left input panel + right output panel
          - bottom    : controls bar
        """

        # Top area
        top_frame = tk.Frame(self.root, bg=theme.BG_PRIMARY)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))

        # Left panel — process input
        self.left_frame = tk.Frame(
            top_frame,
            bg=theme.BG_SECONDARY,
            width=370,
        )
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 8))
        self.left_frame.pack_propagate(False)

        # Right panel — chart + results stacked vertically
        self.right_frame = tk.Frame(top_frame, bg=theme.BG_SECONDARY)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Attach child widgets
        self.process_table = ProcessTableWidget(self.left_frame)
        self.process_table.frame.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=10
        )

        self.gantt_chart = GanttChartWidget(self.right_frame)
        self.gantt_chart.frame.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=(10, 4)
        )

        self.results_table = ResultsTableWidget(self.right_frame)
        self.results_table.frame.pack(
            fill=tk.X, padx=10, pady=(0, 10)
        )

        # Bottom controls bar
        self.controls_bar = ControlsBarWidget(self.root)
        self.controls_bar.frame.pack(fill=tk.X, padx=10, pady=10)

    # ------------------------------------------------------------------
    # Wiring
    # ------------------------------------------------------------------

    def _wire_controls(self):
        """Connect the Run button to the simulation handler."""
        self.controls_bar.set_run_command(self._on_run)

    # ------------------------------------------------------------------
    # Simulation handler
    # ------------------------------------------------------------------

    def _on_run(self):
        """
        Called when the Run button is clicked.
        Reads processes and settings, dispatches to the scheduler,
        and updates the Gantt chart and results table.
        """
        processes = self.process_table.get_processes()

        if not processes:
            messagebox.showwarning(
                "No Processes",
                "Please add at least one process before running.",
            )
            return

        # Resolve the algorithm key from the dropdown label
        label = self.controls_bar.get_algorithm()
        algorithm_key = ALGORITHM_KEY_MAP.get(label, "FCFS")
        quantum = self.controls_bar.get_quantum()

        try:
            result = run_scheduler(algorithm_key, processes, quantum)
        except ValueError as e:
            messagebox.showerror("Simulation Error", str(e))
            return

        # Update the Gantt chart
        self.gantt_chart.render(
            timeline=result["timeline"],
            title=label,
        )

        # Update the results table
        self.results_table.render(
            results=result["results"],
            avg_wt=result["avg_waiting_time"],
            avg_tat=result["avg_turnaround_time"],
        )

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def run(self):
        self.root.mainloop()