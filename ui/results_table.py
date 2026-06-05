# ui/results_table.py
# Results table widget.
# Displays per-process metrics (completion, turnaround, waiting time)
# and average summary rows below the Gantt chart.

import tkinter as tk
from ui import theme


class ResultsTableWidget:
    """
    Renders a styled table of scheduling results.
    Call render(results, avg_wt, avg_tat) to populate it.
    Call clear() to reset it.
    """

    COLUMNS = ["PID", "Arrival", "Burst", "Completion", "Turnaround", "Waiting"]
    COL_WIDTHS = [5, 7, 7, 10, 11, 9]

    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=theme.BG_SECONDARY)

        self._build_header_row()
        self._build_scrollable_area()
        self._build_averages_row()

    # ------------------------------------------------------------------
    # Column headers
    # ------------------------------------------------------------------

    def _build_header_row(self):
        header_frame = tk.Frame(self.frame, bg=theme.BG_PRIMARY)
        header_frame.pack(fill=tk.X, pady=(8, 0))

        for col, (text, width) in enumerate(
            zip(self.COLUMNS, self.COL_WIDTHS)
        ):
            tk.Label(
                header_frame,
                text=text,
                bg=theme.BG_PRIMARY,
                fg=theme.TEXT_HEADER,
                font=theme.FONT_SMALL,
                width=width,
                anchor=tk.CENTER,
            ).grid(row=0, column=col, padx=2, pady=4)

    # ------------------------------------------------------------------
    # Scrollable results area
    # ------------------------------------------------------------------

    def _build_scrollable_area(self):
        container = tk.Frame(self.frame, bg=theme.BG_SECONDARY)
        container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            container,
            bg=theme.BG_SECONDARY,
            highlightthickness=0,
            height=120,
        )
        scrollbar = tk.Scrollbar(
            container,
            orient=tk.VERTICAL,
            command=self.canvas.yview,
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.rows_frame = tk.Frame(self.canvas, bg=theme.BG_SECONDARY)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.rows_frame, anchor=tk.NW
        )

        self.rows_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(
                self.canvas_window, width=e.width
            ),
        )

    # ------------------------------------------------------------------
    # Averages footer
    # ------------------------------------------------------------------

    def _build_averages_row(self):
        self.avg_frame = tk.Frame(self.frame, bg=theme.BG_CARD, pady=6)
        self.avg_frame.pack(fill=tk.X, pady=(4, 0))

        self.avg_label = tk.Label(
            self.avg_frame,
            text="Run the simulator to see results.",
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY,
            font=theme.FONT_SMALL,
        )
        self.avg_label.pack()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(self, results: list[dict], avg_wt: float, avg_tat: float):
        """
        Populates the table with per-process results and averages.

        Args:
            results: List of result dicts from the scheduler.
            avg_wt:  Average waiting time across all processes.
            avg_tat: Average turnaround time across all processes.
        """
        # Clear existing rows
        for child in self.rows_frame.winfo_children():
            child.destroy()

        for i, r in enumerate(results):
            row_bg = (
                theme.BG_CARD if i % 2 == 0 else theme.BG_SECONDARY
            )
            row_frame = tk.Frame(self.rows_frame, bg=row_bg)
            row_frame.pack(fill=tk.X, pady=1)

            values = [
                r["pid"],
                r["arrival"],
                r["burst"],
                r["completion"],
                r["turnaround_time"],
                r["waiting_time"],
            ]

            for value, width in zip(values, self.COL_WIDTHS):
                tk.Label(
                    row_frame,
                    text=str(value),
                    bg=row_bg,
                    fg=theme.TEXT_PRIMARY,
                    font=theme.FONT_MONO,
                    width=width,
                    anchor=tk.CENTER,
                ).pack(side=tk.LEFT, padx=2, pady=3)

        # Update averages footer
        self.avg_label.config(
            text=(
                f"Average Waiting Time: {avg_wt}     "
                f"Average Turnaround Time: {avg_tat}"
            ),
            fg=theme.ACCENT_GREEN,
            font=theme.FONT_LABEL,
        )

    def clear(self):
        """Resets the table to its initial empty state."""
        for child in self.rows_frame.winfo_children():
            child.destroy()
        self.avg_label.config(
            text="Run the simulator to see results.",
            fg=theme.TEXT_SECONDARY,
            font=theme.FONT_SMALL,
        )