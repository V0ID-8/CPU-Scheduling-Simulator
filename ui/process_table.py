# ui/process_table.py
# Widget for displaying the process list and handling process input.
# Users add processes here with arrival time, burst time, and priority.
# This widget is self-contained: it manages its own process data list.

import tkinter as tk
from tkinter import messagebox

from ui import theme


class ProcessTableWidget:
    """
    Renders a labeled input form and a scrollable table of added processes.
    Exposes a get_processes() method for other components to read the data.
    """

    def __init__(self, parent):
        self.parent = parent
        self.processes = []      # List of dicts: {pid, arrival, burst, priority}
        self.pid_counter = 1     # Auto-incremented process ID

        self.frame = tk.Frame(parent, bg=theme.BG_SECONDARY)
        self._build_header()
        self._build_input_form()
        self._build_table()
        self._build_action_buttons()

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------

    def _build_header(self):
        header = tk.Label(
            self.frame,
            text="Process Input",
            bg=theme.BG_SECONDARY,
            fg=theme.TEXT_HEADER,
            font=theme.FONT_HEADER,
            anchor=tk.W,
        )
        header.pack(fill=tk.X, pady=(0, 8))

    # ------------------------------------------------------------------
    # Input form (arrival, burst, priority fields)
    # ------------------------------------------------------------------

    def _build_input_form(self):
        form_frame = tk.Frame(self.frame, bg=theme.BG_CARD, padx=8, pady=8)
        form_frame.pack(fill=tk.X, pady=(0, 8))

        # Row of labels
        labels = ["Arrival Time", "Burst Time", "Priority"]
        for col, text in enumerate(labels):
            tk.Label(
                form_frame,
                text=text,
                bg=theme.BG_CARD,
                fg=theme.TEXT_SECONDARY,
                font=theme.FONT_SMALL,
            ).grid(row=0, column=col, padx=6, pady=(0, 2))

        # Row of entry fields
        self.entry_arrival = self._make_entry(form_frame)
        self.entry_arrival.grid(row=1, column=0, padx=6)

        self.entry_burst = self._make_entry(form_frame)
        self.entry_burst.grid(row=1, column=1, padx=6)

        self.entry_priority = self._make_entry(form_frame)
        self.entry_priority.grid(row=1, column=2, padx=6)

        # Hint below priority
        tk.Label(
            form_frame,
            text="Priority: lower number = higher priority",
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY,
            font=theme.FONT_SMALL,
        ).grid(row=2, column=0, columnspan=3, pady=(6, 0))

    def _make_entry(self, parent) -> tk.Entry:
        """Creates a styled single-line entry field."""
        return tk.Entry(
            parent,
            width=theme.INPUT_WIDTH,
            bg=theme.BG_PRIMARY,
            fg=theme.TEXT_PRIMARY,
            insertbackground=theme.TEXT_PRIMARY,
            relief=tk.FLAT,
            font=theme.FONT_MONO,
            justify=tk.CENTER,
        )

    # ------------------------------------------------------------------
    # Process table (column headers + scrollable rows)
    # ------------------------------------------------------------------

    def _build_table(self):
        # Column headers
        headers_frame = tk.Frame(self.frame, bg=theme.BG_PRIMARY)
        headers_frame.pack(fill=tk.X)

        columns = ["PID", "Arrival", "Burst", "Priority"]
        col_widths = [4, 7, 7, 7]

        for col, (text, width) in enumerate(zip(columns, col_widths)):
            tk.Label(
                headers_frame,
                text=text,
                bg=theme.BG_PRIMARY,
                fg=theme.TEXT_HEADER,
                font=theme.FONT_SMALL,
                width=width,
                anchor=tk.CENTER,
            ).grid(row=0, column=col, padx=2, pady=4)

        # Scrollable canvas for process rows
        canvas_container = tk.Frame(self.frame, bg=theme.BG_SECONDARY)
        canvas_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            canvas_container,
            bg=theme.BG_SECONDARY,
            highlightthickness=0,
            height=280,
        )
        scrollbar = tk.Scrollbar(
            canvas_container,
            orient=tk.VERTICAL,
            command=self.canvas.yview,
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Inner frame inside canvas holds the actual rows
        self.rows_frame = tk.Frame(self.canvas, bg=theme.BG_SECONDARY)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.rows_frame, anchor=tk.NW
        )

        self.rows_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_frame_configure(self, event):
        """Update scroll region when rows are added or removed."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Keep the inner frame width in sync with the canvas width."""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    # ------------------------------------------------------------------
    # Add / Remove buttons
    # ------------------------------------------------------------------

    def _build_action_buttons(self):
        btn_frame = tk.Frame(self.frame, bg=theme.BG_SECONDARY)
        btn_frame.pack(fill=tk.X, pady=(8, 0))

        add_btn = tk.Button(
            btn_frame,
            text="Add Process",
            command=self._add_process,
            bg=theme.ACCENT_BLUE,
            fg=theme.BG_PRIMARY,
            font=theme.FONT_LABEL,
            relief=tk.FLAT,
            cursor="hand2",
            width=theme.BTN_WIDTH,
        )
        add_btn.pack(side=tk.LEFT, padx=(0, 8))

        remove_btn = tk.Button(
            btn_frame,
            text="Remove Last",
            command=self._remove_last,
            bg=theme.ACCENT_RED,
            fg=theme.BG_PRIMARY,
            font=theme.FONT_LABEL,
            relief=tk.FLAT,
            cursor="hand2",
            width=theme.BTN_WIDTH,
        )
        remove_btn.pack(side=tk.LEFT)

        clear_btn = tk.Button(
            btn_frame,
            text="Clear All",
            command=self._clear_all,
            bg=theme.TEXT_SECONDARY,
            fg=theme.TEXT_HEADER,
            font=theme.FONT_LABEL,
            relief=tk.FLAT,
            cursor="hand2",
            width=theme.BTN_WIDTH,
        )
        clear_btn.pack(side=tk.LEFT, padx=(8, 0))

    # ------------------------------------------------------------------
    # Process management logic
    # ------------------------------------------------------------------

    def _add_process(self):
        """Validates inputs, adds a process to the list, and renders a new row."""
        arrival_str = self.entry_arrival.get().strip()
        burst_str = self.entry_burst.get().strip()
        priority_str = self.entry_priority.get().strip()

        # Validate: all fields must be filled with non-negative integers
        if not arrival_str or not burst_str or not priority_str:
            messagebox.showwarning("Input Error", "Please fill in all three fields.")
            return

        try:
            arrival = int(arrival_str)
            burst = int(burst_str)
            priority = int(priority_str)
        except ValueError:
            messagebox.showwarning("Input Error", "All values must be whole numbers.")
            return

        if arrival < 0 or burst <= 0 or priority < 0:
            messagebox.showwarning(
                "Input Error",
                "Arrival >= 0, Burst > 0, Priority >= 0.",
            )
            return

        process = {
            "pid": f"P{self.pid_counter}",
            "arrival": arrival,
            "burst": burst,
            "priority": priority,
        }
        self.processes.append(process)
        self.pid_counter += 1

        self._render_row(process)
        self._clear_entries()

    def _remove_last(self):
        """Removes the most recently added process."""
        if not self.processes:
            return
        self.processes.pop()
        self.pid_counter -= 1

        # Destroy the last row widget in rows_frame
        children = self.rows_frame.winfo_children()
        if children:
            children[-1].destroy()

    def _clear_all(self):
        """Removes all processes from the list and clears all rows."""
        self.processes.clear()
        self.pid_counter = 1
        for child in self.rows_frame.winfo_children():
            child.destroy()

    def _clear_entries(self):
        """Clears the input fields after a successful add."""
        self.entry_arrival.delete(0, tk.END)
        self.entry_burst.delete(0, tk.END)
        self.entry_priority.delete(0, tk.END)
        self.entry_arrival.focus()

    # ------------------------------------------------------------------
    # Row rendering
    # ------------------------------------------------------------------

    def _render_row(self, process: dict):
        """Creates a single styled row in the table for the given process."""
        row_bg = theme.BG_CARD if len(self.processes) % 2 == 0 else theme.BG_SECONDARY

        row_frame = tk.Frame(self.rows_frame, bg=row_bg)
        row_frame.pack(fill=tk.X, pady=1)

        values = [
            process["pid"],
            process["arrival"],
            process["burst"],
            process["priority"],
        ]
        col_widths = [4, 7, 7, 7]

        for value, width in zip(values, col_widths):
            tk.Label(
                row_frame,
                text=str(value),
                bg=row_bg,
                fg=theme.TEXT_PRIMARY,
                font=theme.FONT_MONO,
                width=width,
                anchor=tk.CENTER,
            ).pack(side=tk.LEFT, padx=2, pady=4)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_processes(self) -> list[dict]:
        """Returns the current list of processes for use by the scheduler."""
        return self.processes