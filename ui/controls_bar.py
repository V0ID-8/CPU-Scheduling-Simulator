# ui/controls_bar.py
# Bottom controls bar widget.
# Contains the algorithm dropdown, quantum input, and Run button.
# The Run button logic will be wired up in Step 5 (algorithm integration).

import tkinter as tk
from tkinter import ttk

from ui import theme


class ControlsBarWidget:
    """
    Horizontal bar at the bottom of the window.
    Exposes:
      - get_algorithm()  : returns the selected algorithm name as a string
      - get_quantum()    : returns the quantum value as an int (for Round Robin)
      - set_run_command(): wires an external callback to the Run button
    """

    ALGORITHMS = [
        "First Come First Served (FCFS)",
        "Shortest Job First (SJF)",
        "Round Robin (RR)",
        "Priority Scheduling",
    ]

    def __init__(self, parent):
        self.parent = parent

        self.frame = tk.Frame(parent, bg=theme.BG_SECONDARY, pady=8, padx=10)
        self._build_controls()

    def _build_controls(self):
        # --- Algorithm label and dropdown ---
        tk.Label(
            self.frame,
            text="Algorithm:",
            bg=theme.BG_SECONDARY,
            fg=theme.TEXT_SECONDARY,
            font=theme.FONT_LABEL,
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.algorithm_var = tk.StringVar(value=self.ALGORITHMS[0])

        algorithm_menu = ttk.Combobox(
            self.frame,
            textvariable=self.algorithm_var,
            values=self.ALGORITHMS,
            state="readonly",
            width=28,
            font=theme.FONT_LABEL,
        )
        algorithm_menu.pack(side=tk.LEFT, padx=(0, 20))

        # --- Quantum label and entry ---
        self.quantum_label = tk.Label(
            self.frame,
            text="Quantum:",
            bg=theme.BG_SECONDARY,
            fg=theme.ACCENT_YELLOW,
            font=theme.FONT_LABEL,
        )
        self.quantum_label.pack(side=tk.LEFT, padx=(0, 6))

        self.entry_quantum = tk.Entry(
            self.frame,
            width=5,
            bg=theme.BG_PRIMARY,
            fg=theme.TEXT_PRIMARY,
            insertbackground=theme.TEXT_PRIMARY,
            relief=tk.FLAT,
            font=theme.FONT_MONO,
            justify=tk.CENTER,
        )
        self.entry_quantum.insert(0, "2")
        self.entry_quantum.pack(side=tk.LEFT, padx=(0, 20))

        # Disable quantum input unless Round Robin is selected
        self._toggle_quantum()
        self.algorithm_var.trace_add("write", lambda *_: self._toggle_quantum())

        # --- Run button ---
        self.run_button = tk.Button(
            self.frame,
            text="Run Simulation",
            bg=theme.ACCENT_GREEN,
            fg=theme.BG_PRIMARY,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            width=14,
            command=self._on_run,
        )
        self.run_button.pack(side=tk.RIGHT)

        # Placeholder: wired in Step 5
        self._run_callback = None

    # ------------------------------------------------------------------
    # Quantum toggle
    # ------------------------------------------------------------------

    def _toggle_quantum(self):
        """
        Enables the quantum entry only when Round Robin is selected.
        Disables and grays it out for all other algorithms.
        """
        if "Round Robin" in self.algorithm_var.get():
            self.entry_quantum.config(state=tk.NORMAL, fg=theme.TEXT_PRIMARY)
            self.quantum_label.config(fg=theme.ACCENT_YELLOW)
        else:
            self.entry_quantum.config(state=tk.DISABLED, fg=theme.TEXT_SECONDARY)
            self.quantum_label.config(fg=theme.TEXT_SECONDARY)

    # ------------------------------------------------------------------
    # Run button
    # ------------------------------------------------------------------

    def _on_run(self):
        """Calls the registered run callback if one exists."""
        if self._run_callback:
            self._run_callback()

    def set_run_command(self, callback):
        """Register an external function to call when Run is clicked."""
        self._run_callback = callback

    # ------------------------------------------------------------------
    # Public getters
    # ------------------------------------------------------------------

    def get_algorithm(self) -> str:
        """Returns the selected algorithm string."""
        return self.algorithm_var.get()

    def get_quantum(self) -> int:
        """Returns the quantum value as an integer. Defaults to 2 on error."""
        try:
            val = int(self.entry_quantum.get().strip())
            return val if val > 0 else 2
        except ValueError:
            return 2