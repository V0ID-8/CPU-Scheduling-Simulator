# CPU Scheduling Simulator

![CPU Scheduling Simulator](assets/screenshot.png)


A desktop application that simulates four classic CPU scheduling algorithms with a real-time Gantt chart and per-process metrics. Built with Python and Tkinter, it makes operating system scheduling theory visual and measurable.

---

## Algorithms Implemented

| Algorithm | Type | Key Property |
|---|---|---|
| First Come First Served (FCFS) | Non-preemptive | Executes in arrival order |
| Shortest Job First (SJF) | Non-preemptive | Picks smallest burst time next |
| Round Robin (RR) | Preemptive | Fixed time quantum per process |
| Priority Scheduling | Non-preemptive | Lowest priority number runs first |

---

## Features

- Add up to 10 processes with configurable arrival time, burst time, and priority
- Switch between all four algorithms from a dropdown menu
- Configurable time quantum for Round Robin
- Gantt chart rendered with Matplotlib showing the full execution timeline
- Per-process results table: completion time, turnaround time, waiting time
- Average waiting time and average turnaround time summary
- Input validation with descriptive error messages
- Dark themed UI built entirely with Tkinter

---

## Project Structure

```
cpu-scheduler/
├── algorithms/
│   ├── fcfs.py          # First Come First Served
│   ├── sjf.py           # Shortest Job First (non-preemptive)
│   ├── round_robin.py   # Round Robin with configurable quantum
│   ├── priority.py      # Priority Scheduling (non-preemptive)
│   └── scheduler.py     # Central algorithm router
├── ui/
│   ├── main_window.py   # Top-level window and layout coordinator
│   ├── process_table.py # Process input form and table widget
│   ├── gantt_chart.py   # Matplotlib Gantt chart embedded in Tkinter
│   ├── results_table.py # Per-process metrics table widget
│   ├── controls_bar.py  # Algorithm selector and run button
│   └── theme.py         # Color, font, and spacing constants
├── utils/
│   ├── metrics.py       # Waiting time and turnaround time calculations
│   └── validators.py    # Input validation helpers
├── main.py              # Application entry point
├── requirements.txt
└── .gitignore
```

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/cpu-scheduler.git
cd cpu-scheduler
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

---

## How to Use

1. Enter an **Arrival Time**, **Burst Time**, and **Priority** for each process
2. Click **Add Process** — the process appears in the table below
3. Select a scheduling algorithm from the dropdown
4. If using Round Robin, set the **Quantum** value
5. Click **Run Simulation**
6. The **Gantt chart** and **results table** update immediately

---

## Metrics Explained

**Waiting Time** — total time a process spent in the ready queue, not executing.
```
Waiting Time = Turnaround Time - Burst Time
```

**Turnaround Time** — total time from arrival to completion.
```
Turnaround Time = Completion Time - Arrival Time
```

---

## Example

Given three processes:

| PID | Arrival | Burst | Priority |
|-----|---------|-------|----------|
| P1  | 0       | 5     | 2        |
| P2  | 1       | 3     | 1        |
| P3  | 2       | 1     | 3        |

FCFS result:
- P1 runs 0→5, P2 runs 5→8, P3 runs 8→9
- Average Waiting Time: 4.0
- Average Turnaround Time: 6.0

---

## Built With

- [Python 3.11](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — GUI framework (standard library)
- [Matplotlib](https://matplotlib.org/) — Gantt chart rendering
- [Pillow](https://python-pillow.org/) — image support

---

## Author

**Talal Al-Bulushi**  
GitHub: [github.com/V0ID-8](https://github.com/V0ID-8)

---
