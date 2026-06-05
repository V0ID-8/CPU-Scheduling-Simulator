# ui/gantt_chart.py
# Gantt chart widget using Matplotlib embedded inside a Tkinter frame.
# Renders the scheduling timeline as a horizontal bar chart.
# Each process gets a consistent color across the chart.

import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ui import theme


# Fixed color palette — one color per process slot (up to 10 processes)
PROCESS_COLORS = [
    "#7aa2f7",  # blue
    "#9ece6a",  # green
    "#f7768e",  # red
    "#e0af68",  # yellow
    "#bb9af7",  # purple
    "#7dcfff",  # cyan
    "#ff9e64",  # orange
    "#c0caf5",  # lavender
    "#73daca",  # teal
    "#f7768e",  # pink
]


class GanttChartWidget:
    """
    Embeds a Matplotlib figure inside a Tkinter frame.
    Call render(timeline, title) to draw a new chart.
    Call clear() to reset to the placeholder state.
    """

    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=theme.BG_SECONDARY)

        # Build the initial empty figure
        self.fig, self.ax = plt.subplots(figsize=(6.2, 2.8))
        self.fig.patch.set_facecolor(theme.BG_SECONDARY)
        self._style_axes()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.configure(bg=theme.BG_SECONDARY)
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self._show_placeholder()

    # ------------------------------------------------------------------
    # Axes styling
    # ------------------------------------------------------------------

    def _style_axes(self):
        """Apply dark theme styling to the Matplotlib axes."""
        self.ax.set_facecolor(theme.BG_PRIMARY)

        for spine in self.ax.spines.values():
            spine.set_edgecolor(theme.TEXT_SECONDARY)

        self.ax.tick_params(colors=theme.TEXT_PRIMARY, labelsize=8)
        self.ax.xaxis.label.set_color(theme.TEXT_PRIMARY)
        self.ax.yaxis.label.set_color(theme.TEXT_PRIMARY)
        self.ax.title.set_color(theme.TEXT_HEADER)

    # ------------------------------------------------------------------
    # Placeholder state
    # ------------------------------------------------------------------

    def _show_placeholder(self):
        """Show a message when no simulation has been run yet."""
        self.ax.clear()
        self._style_axes()
        self.ax.text(
            0.5, 0.5,
            "Run the simulator to see the Gantt chart.",
            ha="center", va="center",
            color=theme.TEXT_SECONDARY,
            fontsize=10,
            transform=self.ax.transAxes,
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    def clear(self):
        """Reset the chart to the placeholder state."""
        self._show_placeholder()

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, timeline: list[dict], title: str = "Gantt Chart"):
        """
        Draws the Gantt chart from a timeline list.

        Args:
            timeline: List of dicts with keys: pid, start, end.
            title:    Chart title (usually the algorithm name).
        """
        self.ax.clear()
        self._style_axes()

        # Assign a consistent color to each unique PID
        unique_pids = list(dict.fromkeys(seg["pid"] for seg in timeline))
        color_map = {
            pid: PROCESS_COLORS[i % len(PROCESS_COLORS)]
            for i, pid in enumerate(unique_pids)
        }

        bar_height = 0.5
        y_center = 0.5  # All bars on a single horizontal row

        for seg in timeline:
            duration = seg["end"] - seg["start"]
            color = color_map[seg["pid"]]

            # Draw the bar
            self.ax.broken_barh(
                [(seg["start"], duration)],
                (y_center - bar_height / 2, bar_height),
                facecolors=color,
                edgecolors=theme.BG_PRIMARY,
                linewidth=1.2,
            )

            # Label the bar with the PID if it is wide enough
            if duration > 0:
                self.ax.text(
                    seg["start"] + duration / 2,
                    y_center,
                    seg["pid"],
                    ha="center",
                    va="center",
                    color=theme.BG_PRIMARY,
                    fontsize=8,
                    fontweight="bold",
                )

        # X-axis tick marks at every segment boundary
        boundaries = sorted(
            set(seg["start"] for seg in timeline) |
            {seg["end"] for seg in timeline}
        )
        self.ax.set_xticks(boundaries)
        self.ax.set_xlim(boundaries[0], boundaries[-1])

        # Hide Y axis — we only have one row
        self.ax.set_yticks([])
        self.ax.set_ylim(0, 1)

        self.ax.set_xlabel("Time", color=theme.TEXT_PRIMARY, fontsize=9)
        self.ax.set_title(title, color=theme.TEXT_HEADER, fontsize=10, pad=8)

        # Legend: one patch per unique PID
        legend_patches = [
            mpatches.Patch(color=color_map[pid], label=pid)
            for pid in unique_pids
        ]
        self.ax.legend(
            handles=legend_patches,
            loc="upper right",
            fontsize=8,
            facecolor=theme.BG_CARD,
            edgecolor=theme.TEXT_SECONDARY,
            labelcolor=theme.TEXT_PRIMARY,
        )

        self.fig.tight_layout()
        self.canvas.draw()